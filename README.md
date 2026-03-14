# Pharma OSD Manufacturing Control Tower

Working prototype for proactive process health monitoring across a five-site oral solid dosage manufacturing network.

## Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL-ready database layer
- Frontend: Next.js, React, Tailwind CSS, Recharts
- Demo mode: synthetic event-driven batch data seeded on startup

## Project Structure

```text
backend/
  main.py
  models.py
  feature_engine.py
  kpi_engine.py
  alerts.py
  sample_data.py
  schema.sql
frontend/
  pages/
  components/
  charts/
```

## Local Run

### 1. Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Default demo database:

- `sqlite:///./pharma_control_tower.db`

To use PostgreSQL instead, set:

```bash
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/pharma_osd
```

API runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Frontend

```bash
cd frontend
npm install
set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

UI runs at [http://127.0.0.1:3000](http://127.0.0.1:3000).

## Included Pages

- `/` Network Control Tower
- `/product-health` Product Health
- `/batch-monitoring` Batch Monitoring
- `/site-benchmarking` Site Benchmarking

## Notes

- The synthetic generator creates five sites, fifty products, and two batches per product per site.
- KPI and alert calculations run automatically after seed generation.
- The API is PostgreSQL-compatible; SQLite is only the default for quick local startup.

## Business Guide

For a business-facing explanation of the use case, demo flow, page meanings, and stakeholder talk track, see [BUSINESS_README.md](C:\Users\vasua\OneDrive\Documents\PHR2\BUSINESS_README.md).

## Deployment Guide

For step-by-step publishing with Render and Vercel, see [DEPLOYMENT_GUIDE.md](C:\Users\vasua\OneDrive\Documents\PHR2\DEPLOYMENT_GUIDE.md).
