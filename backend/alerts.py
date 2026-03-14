from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Alert, KPIMetric, StabilityScore


ALERT_MESSAGES = {
    "Compression_Force_CV": "Compression force variability indicates risk of tablet weight variation. Inspect feeder speed and punch wear.",
    "Granulation_Torque_CV": "Granulation torque variability suggests binder distribution instability. Review binder spray pattern and impeller settings.",
    "Dryer_Temp_Stability": "Dryer temperature instability may affect residual moisture consistency. Inspect airflow and heater control loops.",
    "Tablet_Weight_Variability": "Tablet weight variability is rising. Inspect die fill consistency, feeder tuning, and turret speed.",
    "Coating_Spray_Stability": "Coating spray instability may create film non-uniformity. Inspect nozzle performance and atomization pressure.",
    "Process_Stability_Score": "Process stability score has dropped below the review threshold. Escalate review-by-exception across unit operations.",
}


def generate_alerts(db: Session, batch_id: int):
    db.query(Alert).filter(Alert.batch_id == batch_id).delete()

    metrics = db.execute(select(KPIMetric).where(KPIMetric.batch_id == batch_id)).scalars().all()
    stability = db.get(StabilityScore, batch_id)
    now = datetime.utcnow()
    created = []

    for metric in metrics:
        if metric.metric_score < 60:
            created.append(
                Alert(
                    batch_id=batch_id,
                    product_id=metric.product_id,
                    site_id=metric.site_id,
                    metric_name=metric.metric_name,
                    severity="HIGH" if metric.metric_score < 45 else "MEDIUM",
                    message=ALERT_MESSAGES.get(metric.metric_name, f"{metric.metric_name} breached the proactive threshold."),
                    created_at=now,
                )
            )

    if stability and stability.process_stability_score < 70:
        created.append(
            Alert(
                batch_id=batch_id,
                product_id=stability.product_id,
                site_id=stability.site_id,
                metric_name="Process_Stability_Score",
                severity="HIGH",
                message=ALERT_MESSAGES["Process_Stability_Score"],
                created_at=now,
            )
        )

    for alert in created:
        db.add(alert)
    db.commit()
    return created
