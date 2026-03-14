from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

from sqlalchemy import select
from sqlalchemy.orm import Session

from .alerts import generate_alerts
from .kpi_engine import compute_batch_kpis, compute_process_stability_score
from .models import Batch, PITimeSeries, ProcessStep, Product, Site


SITE_DATA = [
    ("Hyderabad Alpha", "India"),
    ("Basel Prime", "Switzerland"),
    ("Cork Bio", "Ireland"),
    ("New Jersey East", "USA"),
    ("Singapore Nexus", "Singapore"),
]


def seed_demo_data(db: Session):
    existing = db.execute(select(Site.site_id)).first()
    if existing:
        return

    rng = Random(42)
    sites = []
    for idx, (name, country) in enumerate(SITE_DATA, start=1):
        site = Site(site_id=idx, site_name=name, country=country)
        sites.append(site)
        db.add(site)

    products = []
    strengths = ["100 mg", "250 mg", "500 mg", "850 mg", "1 g"]
    product_names = [
        "Metformin",
        "Paracetamol",
        "Atorvastatin",
        "Ibuprofen",
        "Levothyroxine",
        "Amlodipine",
        "Cetirizine",
        "Azithromycin",
        "Losartan",
        "Omeprazole",
    ]
    for idx in range(1, 51):
        product = Product(
            product_id=idx,
            product_name=f"{product_names[(idx - 1) % len(product_names)]} {idx}",
            dosage_form="Tablet",
            strength=strengths[(idx - 1) % len(strengths)],
        )
        products.append(product)
        db.add(product)

    db.commit()

    steps = ["granulation", "drying", "blending", "compression", "coating", "packaging"]
    tag_profiles = {
        "granulation_torque": (42.0, 6.0),
        "drying_temperature": (62.0, 3.5),
        "drying_moisture": (7.0, -0.12),
        "compression_force": (18.0, 1.2),
        "tablet_weight": (620.0, 9.0),
        "ejection_force": (4.4, 0.08),
        "coating_spray_rate": (210.0, 12.0),
        "atomization_pressure": (1.8, 0.09),
    }

    batch_id = 1
    base_start = datetime.utcnow() - timedelta(days=20)
    for site in sites:
        for product in products[:20]:
            for cycle in range(2):
                batch_start = base_start + timedelta(hours=batch_id * 3)
                batch_end = batch_start + timedelta(hours=11)
                batch = Batch(
                    batch_id=batch_id,
                    product_id=product.product_id,
                    site_id=site.site_id,
                    batch_start=batch_start,
                    batch_end=batch_end,
                    status="COMPLETED" if cycle == 0 else "IN_PROGRESS",
                )
                db.add(batch)

                for step_idx, step in enumerate(steps):
                    db.add(
                        ProcessStep(
                            batch_id=batch_id,
                            step_name=step,
                            equipment_id=f"{site.site_id}-{step[:4].upper()}-{(product.product_id % 4) + 1}",
                            start_time=batch_start + timedelta(hours=step_idx * 1.5),
                            end_time=batch_start + timedelta(hours=(step_idx + 1) * 1.5),
                        )
                    )

                for minute in range(60):
                    ts = batch_start + timedelta(minutes=minute)
                    drift = (batch_id % 9) * 0.15
                    _insert_ts(db, batch_id, ts, site.site_id, "GRAN-01", "granulation_torque", tag_profiles["granulation_torque"], rng, drift)
                    _insert_ts(db, batch_id, ts, site.site_id, "DRY-01", "drying_temperature", tag_profiles["drying_temperature"], rng, drift / 3)
                    moisture_start, moisture_slope = tag_profiles["drying_moisture"]
                    moisture_value = max(1.1, moisture_start + (moisture_slope * minute) + rng.uniform(-0.08, 0.08))
                    db.add(PITimeSeries(timestamp=ts, tag_name="drying_moisture", equipment_id="DRY-01", value=moisture_value, batch_id=batch_id))
                    _insert_ts(db, batch_id, ts, site.site_id, "COMP-01", "compression_force", tag_profiles["compression_force"], rng, drift / 4)
                    _insert_ts(db, batch_id, ts, site.site_id, "COMP-01", "tablet_weight", tag_profiles["tablet_weight"], rng, drift * 2)
                    _insert_ts(db, batch_id, ts, site.site_id, "COMP-01", "ejection_force", tag_profiles["ejection_force"], rng, drift / 10)
                    _insert_ts(db, batch_id, ts, site.site_id, "COAT-01", "coating_spray_rate", tag_profiles["coating_spray_rate"], rng, drift * 1.5)
                    _insert_ts(db, batch_id, ts, site.site_id, "COAT-01", "atomization_pressure", tag_profiles["atomization_pressure"], rng, drift / 25)

                batch_id += 1

    db.commit()

    for batch_num in range(1, batch_id):
        compute_batch_kpis(db, batch_num)
        compute_process_stability_score(db, batch_num)
        generate_alerts(db, batch_num)


def _insert_ts(db, batch_id, timestamp, site_id, equipment_id, tag_name, profile, rng, drift):
    base, noise = profile
    value = base + drift + rng.uniform(-noise, noise)
    db.add(
        PITimeSeries(
            timestamp=timestamp,
            tag_name=tag_name,
            equipment_id=equipment_id,
            value=float(value),
            batch_id=batch_id,
        )
    )
