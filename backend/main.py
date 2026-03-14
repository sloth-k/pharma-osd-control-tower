from __future__ import annotations

from collections import defaultdict

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .models import Alert, Batch, KPIMetric, Product, Site, StabilityScore
from .sample_data import seed_demo_data
from .schemas import AlertOut, BatchOut, KPIMetricOut, ProductOut, SiteOut, StabilityScoreOut


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pharma OSD Manufacturing Control Tower")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sites", response_model=list[SiteOut])
def get_sites(db: Session = Depends(get_db)):
    return db.execute(select(Site).order_by(Site.site_name)).scalars().all()


@app.get("/products", response_model=list[ProductOut])
def get_products(limit: int = Query(default=100, le=1000), db: Session = Depends(get_db)):
    return db.execute(select(Product).order_by(Product.product_name).limit(limit)).scalars().all()


@app.get("/batches", response_model=list[BatchOut])
def get_batches(site_id: int | None = None, product_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Batch).order_by(desc(Batch.batch_start)).limit(100)
    if site_id:
        stmt = stmt.where(Batch.site_id == site_id)
    if product_id:
        stmt = stmt.where(Batch.product_id == product_id)
    return db.execute(stmt).scalars().all()


@app.get("/kpis", response_model=list[KPIMetricOut])
def get_kpis(batch_id: int | None = None, product_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(KPIMetric).order_by(desc(KPIMetric.computed_at))
    if batch_id:
        stmt = stmt.where(KPIMetric.batch_id == batch_id)
    if product_id:
        stmt = stmt.where(KPIMetric.product_id == product_id)
    return db.execute(stmt.limit(500)).scalars().all()


@app.get("/alerts", response_model=list[AlertOut])
def get_alerts(db: Session = Depends(get_db)):
    return db.execute(select(Alert).order_by(desc(Alert.created_at)).limit(50)).scalars().all()


@app.get("/stability_scores", response_model=list[StabilityScoreOut])
def get_stability_scores(db: Session = Depends(get_db)):
    return db.execute(
        select(StabilityScore).order_by(desc(StabilityScore.process_stability_score)).limit(200)
    ).scalars().all()


@app.get("/site_benchmark")
def get_site_benchmark(product_id: int | None = None, db: Session = Depends(get_db)):
    stmt = (
        select(
            StabilityScore.product_id,
            StabilityScore.site_id,
            func.avg(StabilityScore.process_stability_score).label("avg_pss"),
        )
        .group_by(StabilityScore.product_id, StabilityScore.site_id)
        .order_by(StabilityScore.product_id, StabilityScore.site_id)
    )
    if product_id:
        stmt = stmt.where(StabilityScore.product_id == product_id)

    rows = db.execute(stmt).all()
    return [
        {"product_id": row.product_id, "site_id": row.site_id, "avg_pss": round(row.avg_pss, 2)}
        for row in rows
    ]


@app.get("/product_health/{product_id}")
def get_product_health(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    stability_rows = db.execute(
        select(StabilityScore).where(StabilityScore.product_id == product_id).order_by(desc(StabilityScore.computed_at))
    ).scalars().all()
    kpi_rows = db.execute(
        select(KPIMetric).where(KPIMetric.product_id == product_id).order_by(KPIMetric.computed_at.asc())
    ).scalars().all()

    stage_averages = defaultdict(list)
    for row in stability_rows:
        stage_averages["granulation"].append(row.granulation_score)
        stage_averages["drying"].append(row.drying_score)
        stage_averages["blending"].append(row.blending_score)
        stage_averages["compression"].append(row.compression_score)
        stage_averages["coating"].append(row.coating_score)

    stages = {
        stage: round(sum(values) / len(values), 2) if values else 0.0 for stage, values in stage_averages.items()
    }

    trend_groups = defaultdict(list)
    for metric in kpi_rows:
        trend_groups[metric.metric_name].append(
            {
                "batch_id": metric.batch_id,
                "score": round(metric.metric_score, 2),
                "value": round(metric.metric_value, 2),
                "step_name": metric.step_name,
            }
        )

    return {
        "product": ProductOut.model_validate(product),
        "stage_scores": stages,
        "kpi_trends": trend_groups,
        "recent_batches": [StabilityScoreOut.model_validate(row) for row in stability_rows[:10]],
    }
