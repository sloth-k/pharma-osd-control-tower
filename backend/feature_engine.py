from __future__ import annotations

from datetime import datetime
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import PITimeSeries, ProcessFeature


def _series(db: Session, batch_id: int, tag_name: str):
    stmt = (
        select(PITimeSeries)
        .where(PITimeSeries.batch_id == batch_id, PITimeSeries.tag_name == tag_name)
        .order_by(PITimeSeries.timestamp.asc())
    )
    return db.execute(stmt).scalars().all()


def _values(records):
    return [record.value for record in records]


def _mean(values):
    return mean(values) if values else 0.0


def _cv(values):
    if not values:
        return 0.0
    avg = _mean(values)
    if avg == 0:
        return 0.0
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    return (variance**0.5 / avg) * 100


def _slope(values):
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / (len(values) - 1)


def _integral(values):
    if len(values) < 2:
        return sum(values)
    return sum((values[idx] + values[idx - 1]) / 2 for idx in range(1, len(values)))


def compute_granulation_features(db: Session, batch_id: int):
    torque_values = _values(_series(db, batch_id, "granulation_torque"))
    features = {
        "torque_mean": _mean(torque_values),
        "torque_cv": _cv(torque_values),
        "granulation_energy": _integral(torque_values),
        "torque_slope": _slope(torque_values),
    }
    return _persist_features(db, batch_id, "granulation", features)


def compute_drying_features(db: Session, batch_id: int):
    temp_values = _values(_series(db, batch_id, "drying_temperature"))
    moisture_values = _values(_series(db, batch_id, "drying_moisture"))
    rate = 0.0
    if len(moisture_values) > 1:
        rate = max((moisture_values[0] - moisture_values[-1]) / len(moisture_values), 0.0)
    features = {
        "dryer_temp_cv": _cv(temp_values),
        "moisture_removal_rate": rate,
    }
    return _persist_features(db, batch_id, "drying", features)


def compute_compression_features(db: Session, batch_id: int):
    force_values = _values(_series(db, batch_id, "compression_force"))
    weight_values = _values(_series(db, batch_id, "tablet_weight"))
    ejection_values = _values(_series(db, batch_id, "ejection_force"))
    features = {
        "compression_force_cv": _cv(force_values),
        "tablet_weight_cv": _cv(weight_values),
        "ejection_force_trend": _slope(ejection_values),
    }
    return _persist_features(db, batch_id, "compression", features)


def compute_coating_features(db: Session, batch_id: int):
    spray_values = _values(_series(db, batch_id, "coating_spray_rate"))
    atomization_values = _values(_series(db, batch_id, "atomization_pressure"))
    features = {
        "spray_rate_cv": _cv(spray_values),
        "atomization_pressure_cv": _cv(atomization_values),
    }
    return _persist_features(db, batch_id, "coating", features)


def compute_all_features(db: Session, batch_id: int):
    features = {}
    for calculator in (
        compute_granulation_features,
        compute_drying_features,
        compute_compression_features,
        compute_coating_features,
    ):
        features.update(calculator(db, batch_id))
    return features


def _persist_features(db: Session, batch_id: int, step_name: str, features: dict[str, float]):
    db.query(ProcessFeature).filter(
        ProcessFeature.batch_id == batch_id, ProcessFeature.step_name == step_name
    ).delete()
    now = datetime.utcnow()
    for name, value in features.items():
        db.add(
            ProcessFeature(
                batch_id=batch_id,
                step_name=step_name,
                feature_name=name,
                feature_value=float(value),
                computed_at=now,
            )
        )
    db.commit()
    return features
