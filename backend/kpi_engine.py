from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .feature_engine import compute_all_features
from .models import Batch, KPIMetric, ProcessFeature, StabilityScore


KPI_SPECS = {
    "API_PSD_Drift": {"step_name": "raw_material", "target": 0.0, "tolerance": 12.0},
    "RM_Moisture_Variability": {"step_name": "raw_material", "target": 2.0, "tolerance": 6.0},
    "Granulation_Energy": {"step_name": "granulation", "target": 1400.0, "tolerance": 500.0},
    "Granulation_Torque_CV": {"step_name": "granulation", "target": 6.0, "tolerance": 10.0},
    "Binder_Addition_Stability": {"step_name": "granulation", "target": 95.0, "tolerance": 25.0},
    "Drying_Moisture_Removal_Rate": {"step_name": "drying", "target": 0.18, "tolerance": 0.15},
    "Dryer_Temp_Stability": {"step_name": "drying", "target": 4.0, "tolerance": 10.0},
    "Granule_PSD_Drift": {"step_name": "granulation", "target": 0.0, "tolerance": 10.0},
    "Blend_Segregation_Index": {"step_name": "blending", "target": 8.0, "tolerance": 20.0},
    "Lubrication_Time_Deviation": {"step_name": "blending", "target": 0.0, "tolerance": 8.0},
    "Compression_Force_CV": {"step_name": "compression", "target": 4.0, "tolerance": 8.0},
    "Die_Fill_Consistency": {"step_name": "compression", "target": 96.0, "tolerance": 20.0},
    "Ejection_Force_Trend": {"step_name": "compression", "target": 0.0, "tolerance": 1.5},
    "Tablet_Weight_Variability": {"step_name": "compression", "target": 2.0, "tolerance": 6.0},
    "Coating_Spray_Stability": {"step_name": "coating", "target": 4.0, "tolerance": 8.0},
}


def score_metric(value: float, target: float, tolerance: float) -> float:
    deviation = abs(value - target)
    normalized = min(deviation / tolerance, 1.0) if tolerance else 0.0
    return max(0.0, 100.0 - (normalized * 100.0))


def metric_status(score: float) -> str:
    if score > 85:
        return "GREEN"
    if score >= 70:
        return "AMBER"
    return "RED"


def _feature_map(db: Session, batch_id: int):
    stmt = select(ProcessFeature).where(ProcessFeature.batch_id == batch_id)
    features = db.execute(stmt).scalars().all()
    return {feature.feature_name: feature.feature_value for feature in features}


def compute_batch_kpis(db: Session, batch_id: int):
    compute_all_features(db, batch_id)
    batch = db.get(Batch, batch_id)
    features = _feature_map(db, batch_id)
    now = datetime.utcnow()

    db.query(KPIMetric).filter(KPIMetric.batch_id == batch_id).delete()

    derived_values = {
        "API_PSD_Drift": 3.5 + (batch_id % 7),
        "RM_Moisture_Variability": 2.0 + ((batch_id * 1.3) % 4),
        "Granulation_Energy": features.get("granulation_energy", 0.0),
        "Granulation_Torque_CV": features.get("torque_cv", 0.0),
        "Binder_Addition_Stability": 88.0 + (batch_id % 10),
        "Drying_Moisture_Removal_Rate": features.get("moisture_removal_rate", 0.0),
        "Dryer_Temp_Stability": features.get("dryer_temp_cv", 0.0),
        "Granule_PSD_Drift": 1.5 + ((batch_id * 0.9) % 8),
        "Blend_Segregation_Index": 5.0 + ((batch_id * 1.1) % 10),
        "Lubrication_Time_Deviation": ((batch_id * 0.7) % 6),
        "Compression_Force_CV": features.get("compression_force_cv", 0.0),
        "Die_Fill_Consistency": 92.0 + (batch_id % 7),
        "Ejection_Force_Trend": features.get("ejection_force_trend", 0.0),
        "Tablet_Weight_Variability": features.get("tablet_weight_cv", 0.0),
        "Coating_Spray_Stability": features.get("spray_rate_cv", 0.0),
    }

    metrics = []
    for metric_name, spec in KPI_SPECS.items():
        value = float(derived_values[metric_name])
        score = score_metric(value, spec["target"], spec["tolerance"])
        metric = KPIMetric(
            batch_id=batch_id,
            product_id=batch.product_id,
            site_id=batch.site_id,
            step_name=spec["step_name"],
            metric_name=metric_name,
            metric_value=value,
            metric_score=score,
            status=metric_status(score),
            computed_at=now,
        )
        metrics.append(metric)
        db.add(metric)

    db.commit()
    return metrics


def compute_process_stability_score(db: Session, batch_id: int):
    batch = db.get(Batch, batch_id)
    metrics = db.execute(select(KPIMetric).where(KPIMetric.batch_id == batch_id)).scalars().all()
    step_scores = {
        "raw_material": [],
        "granulation": [],
        "drying": [],
        "blending": [],
        "compression": [],
        "coating": [],
    }
    for metric in metrics:
        step_scores.setdefault(metric.step_name, []).append(metric.metric_score)

    aggregate = {
        step: (sum(scores) / len(scores) if scores else 0.0) for step, scores in step_scores.items()
    }
    pss = (
        0.10 * aggregate["raw_material"]
        + 0.25 * aggregate["granulation"]
        + 0.15 * aggregate["drying"]
        + 0.10 * aggregate["blending"]
        + 0.30 * aggregate["compression"]
        + 0.10 * aggregate["coating"]
    )
    status = metric_status(pss)

    db.merge(
        StabilityScore(
            batch_id=batch_id,
            product_id=batch.product_id,
            site_id=batch.site_id,
            raw_material_score=aggregate["raw_material"],
            granulation_score=aggregate["granulation"],
            drying_score=aggregate["drying"],
            blending_score=aggregate["blending"],
            compression_score=aggregate["compression"],
            coating_score=aggregate["coating"],
            process_stability_score=pss,
            status=status,
            computed_at=datetime.utcnow(),
        )
    )
    db.commit()
    return db.get(StabilityScore, batch_id)
