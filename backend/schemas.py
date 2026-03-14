from datetime import datetime

from pydantic import BaseModel


class SiteOut(BaseModel):
    site_id: int
    site_name: str
    country: str

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    product_id: int
    product_name: str
    dosage_form: str
    strength: str

    class Config:
        from_attributes = True


class BatchOut(BaseModel):
    batch_id: int
    product_id: int
    site_id: int
    batch_start: datetime
    batch_end: datetime | None
    status: str

    class Config:
        from_attributes = True


class KPIMetricOut(BaseModel):
    metric_id: int
    batch_id: int
    product_id: int
    site_id: int
    step_name: str
    metric_name: str
    metric_value: float
    metric_score: float
    status: str
    computed_at: datetime

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    alert_id: int
    batch_id: int
    product_id: int
    site_id: int
    metric_name: str
    severity: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class StabilityScoreOut(BaseModel):
    batch_id: int
    product_id: int
    site_id: int
    raw_material_score: float
    granulation_score: float
    drying_score: float
    blending_score: float
    compression_score: float
    coating_score: float
    process_stability_score: float
    status: str
    computed_at: datetime

    class Config:
        from_attributes = True
