CREATE TABLE sites (
    site_id INTEGER PRIMARY KEY,
    site_name VARCHAR(120) NOT NULL UNIQUE,
    country VARCHAR(80) NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(120) NOT NULL,
    dosage_form VARCHAR(80) NOT NULL,
    strength VARCHAR(40) NOT NULL
);

CREATE TABLE batches (
    batch_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    site_id INTEGER NOT NULL REFERENCES sites(site_id),
    batch_start TIMESTAMP NOT NULL,
    batch_end TIMESTAMP NULL,
    status VARCHAR(40) NOT NULL
);

CREATE TABLE process_steps (
    step_id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id),
    step_name VARCHAR(80) NOT NULL,
    equipment_id VARCHAR(80) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL
);

CREATE TABLE pi_timeseries (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    tag_name VARCHAR(120) NOT NULL,
    equipment_id VARCHAR(80) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id)
);

CREATE TABLE process_features (
    feature_id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id),
    step_name VARCHAR(80) NOT NULL,
    feature_name VARCHAR(120) NOT NULL,
    feature_value DOUBLE PRECISION NOT NULL,
    computed_at TIMESTAMP NOT NULL
);

CREATE TABLE kpi_metrics (
    metric_id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    site_id INTEGER NOT NULL REFERENCES sites(site_id),
    step_name VARCHAR(80) NOT NULL,
    metric_name VARCHAR(120) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    metric_score DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) NOT NULL,
    computed_at TIMESTAMP NOT NULL
);

CREATE TABLE alerts (
    alert_id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(batch_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    site_id INTEGER NOT NULL REFERENCES sites(site_id),
    metric_name VARCHAR(120) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE stability_scores (
    batch_id INTEGER PRIMARY KEY REFERENCES batches(batch_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    site_id INTEGER NOT NULL REFERENCES sites(site_id),
    raw_material_score DOUBLE PRECISION NOT NULL,
    granulation_score DOUBLE PRECISION NOT NULL,
    drying_score DOUBLE PRECISION NOT NULL,
    blending_score DOUBLE PRECISION NOT NULL,
    compression_score DOUBLE PRECISION NOT NULL,
    coating_score DOUBLE PRECISION NOT NULL,
    process_stability_score DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) NOT NULL,
    computed_at TIMESTAMP NOT NULL
);
