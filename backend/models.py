from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Site(Base):
    __tablename__ = "sites"

    site_id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(120), nullable=False, unique=True)
    country = Column(String(80), nullable=False)

    batches = relationship("Batch", back_populates="site")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(120), nullable=False)
    dosage_form = Column(String(80), nullable=False)
    strength = Column(String(40), nullable=False)

    batches = relationship("Batch", back_populates="product")


class Batch(Base):
    __tablename__ = "batches"

    batch_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id"), nullable=False, index=True)
    batch_start = Column(DateTime, nullable=False)
    batch_end = Column(DateTime, nullable=True)
    status = Column(String(40), nullable=False)

    product = relationship("Product", back_populates="batches")
    site = relationship("Site", back_populates="batches")
    process_steps = relationship("ProcessStep", back_populates="batch")


class ProcessStep(Base):
    __tablename__ = "process_steps"

    step_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False, index=True)
    step_name = Column(String(80), nullable=False, index=True)
    equipment_id = Column(String(80), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    batch = relationship("Batch", back_populates="process_steps")


class PITimeSeries(Base):
    __tablename__ = "pi_timeseries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    tag_name = Column(String(120), nullable=False, index=True)
    equipment_id = Column(String(80), nullable=False, index=True)
    value = Column(Float, nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False, index=True)


class ProcessFeature(Base):
    __tablename__ = "process_features"

    feature_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False, index=True)
    step_name = Column(String(80), nullable=False, index=True)
    feature_name = Column(String(120), nullable=False, index=True)
    feature_value = Column(Float, nullable=False)
    computed_at = Column(DateTime, nullable=False)


class KPIMetric(Base):
    __tablename__ = "kpi_metrics"

    metric_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id"), nullable=False, index=True)
    step_name = Column(String(80), nullable=False, index=True)
    metric_name = Column(String(120), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_score = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, index=True)
    computed_at = Column(DateTime, nullable=False)


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id"), nullable=False, index=True)
    metric_name = Column(String(120), nullable=False, index=True)
    severity = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)


class StabilityScore(Base):
    __tablename__ = "stability_scores"

    batch_id = Column(Integer, ForeignKey("batches.batch_id"), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    site_id = Column(Integer, ForeignKey("sites.site_id"), nullable=False, index=True)
    raw_material_score = Column(Float, nullable=False)
    granulation_score = Column(Float, nullable=False)
    drying_score = Column(Float, nullable=False)
    blending_score = Column(Float, nullable=False)
    compression_score = Column(Float, nullable=False)
    coating_score = Column(Float, nullable=False)
    process_stability_score = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, index=True)
    computed_at = Column(DateTime, nullable=False)
