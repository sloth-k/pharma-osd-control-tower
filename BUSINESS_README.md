# Pharma OSD Manufacturing Control Tower

## What This Prototype Is

This is a business-facing prototype of a Pharma Oral Solid Dosage Manufacturing Control Tower.

It is designed to help manufacturing, quality, and technical operations teams monitor early signals of process instability across multiple sites before those issues become:

- batch deviations
- quality events
- yield loss
- OOS or OOT results
- rework or release delays

The prototype simulates a network of 5 manufacturing sites producing tablet products and shows how leaders can move from lagging quality reporting to proactive process health monitoring.

## Business Problem It Solves

Most manufacturing reporting tells us what went wrong after the batch is already at risk or complete.

This dashboard is built around leading indicators. It highlights early process drift during unit operations such as:

- granulation
- drying
- blending
- compression
- coating
- packaging

The goal is to support review-by-exception. Instead of manually reviewing every batch in the same way, teams can focus attention on products, sites, and stages that show risk signals first.

## Intended Users

- Site Heads
- Manufacturing Operations Leaders
- Process Engineers
- Technical Services / MSAT teams
- Quality Operations
- Plant Leadership
- Network Manufacturing Excellence teams

## Core Business Value

### 1. Earlier risk detection

The system surfaces instability before final QC results or batch closure.

### 2. Faster decision making

Leaders can quickly identify:

- which site is drifting
- which product is unstable
- which unit operation needs intervention
- which batch needs immediate attention

### 3. Better cross-site comparison

The same product can be compared across sites to identify best-performing locations and transfer learnings.

### 4. Review-by-exception

Instead of reviewing hundreds of products and batches manually, the dashboard brings the highest-risk items to the top.

## What Data Sources It Represents

The prototype is aligned to a typical pharma digital manufacturing architecture:

- MES events for batch and process step completion
- PI Historian for time-series equipment and process parameters
- LIMS for raw material and quality-related attributes
- event-driven KPI calculation after process step completion

In the prototype, synthetic data is used to simulate this environment.

## Key Business Concepts

### Leading Indicator KPIs

These are early warning indicators of process health, such as:

- raw material moisture variability
- granulation energy
- granulation torque variation
- drying moisture removal rate
- compression force variability
- tablet weight variability
- coating spray stability

These are not final quality outcomes. They are predictive process signals that indicate whether the batch may be trending toward trouble.

### Process Stability Score

The Process Stability Score is a single weighted score that summarizes batch health across major manufacturing stages.

It gives business users a simple answer to:

"How stable is this product or batch right now?"

Higher is better.

### Alerts

Alerts are triggered when a KPI score or overall stability score crosses a risk threshold.

This helps teams prioritize action and escalate only where needed.

## What Each Dashboard Page Means

### 1. Network Control Tower

Business purpose:
Provide a leadership-level summary of overall network health.

What it shows:

- product vs site stability matrix
- traffic-light style health indicators
- top alerts requiring attention
- average Process Stability Score by site

How to talk about it:
"This is the executive summary view. It shows where process stability is strong, where it is deteriorating, and which alerts require intervention."

### 2. Product Health

Business purpose:
Show how one product is performing across manufacturing stages.

What it shows:

- granulation score
- drying score
- blending score
- compression score
- coating score
- KPI trend charts over recent batches

How to talk about it:
"This view helps us understand whether risk is concentrated in one stage, such as compression or drying, rather than treating the product as a single black box."

### 3. Batch Monitoring

Business purpose:
Give operations teams a near-real-time view of active batch health.

What it shows:

- gauges for critical KPI scores
- recent KPI signal trend view

How to talk about it:
"This page is the operational watchlist. It helps teams act while the process is still running instead of waiting for post-batch reporting."

### 4. Site Benchmarking

Business purpose:
Compare the same product across sites.

What it shows:

- heatmap of Process Stability Score by product and site

How to talk about it:
"This lets us identify where the same product is most stable across the network and where targeted improvement or knowledge transfer may be needed."

## Suggested Leadership Demo Flow

Use this 3 to 5 minute sequence.

### Opening statement

"This prototype demonstrates how we can shift from lagging quality metrics to proactive process health monitoring across OSD manufacturing."

### Step 1. Show Network Control Tower

Open:
[http://localhost:3000/](http://localhost:3000/)

Say:
"At the network level, we can immediately see which sites and products are stable, where the alerts are concentrated, and where to focus operational review."

### Step 2. Show Product Health

Open:
[http://localhost:3000/product-health](http://localhost:3000/product-health)

Say:
"For a selected product, we can see which manufacturing stages are driving risk and how the leading indicators have moved across recent batches."

### Step 3. Show Batch Monitoring

Open:
[http://localhost:3000/batch-monitoring](http://localhost:3000/batch-monitoring)

Say:
"This gives the plant team a near-real-time watchlist of critical process signals so intervention can happen before deviations occur."

### Step 4. Show Site Benchmarking

Open:
[http://localhost:3000/site-benchmarking](http://localhost:3000/site-benchmarking)

Say:
"This helps compare the same product across sites, identify stronger process capability, and support cross-site learning and standardization."

### Closing statement

"The strategic value is earlier visibility, faster intervention, and a more scalable review-by-exception model for network manufacturing."

## How To Use This Prototype In A Business Discussion

This prototype is best positioned as:

- a vision demo
- a digital manufacturing use case
- a control tower concept for proactive process health
- a starting point for future MES, PI, and LIMS integration

It should not be positioned as a validated GxP system or production-ready release.

## What Is Real vs Simulated

Real in this prototype:

- data model
- KPI scoring logic
- alerting concept
- business workflows
- dashboard structure
- multi-site operating model

Simulated in this prototype:

- batch data
- PI historian signals
- product master set
- real-time integration
- business thresholds

## Recommended Business Next Steps

- align KPI definitions with manufacturing science and technology teams
- validate thresholds with site process experts
- connect to MES step events
- connect PI historian time-series tags
- incorporate LIMS raw material attributes
- define user roles for plant, network, and quality teams
- prioritize a pilot product family and 1 or 2 sites

## How To Run The Demo

### Backend

From `C:\Users\vasua\OneDrive\Documents\PHR2`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt
uvicorn backend.main:app --reload
```

Backend URL:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

Health check:
[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Frontend

From `C:\Users\vasua\OneDrive\Documents\PHR2\frontend`:

```powershell
npm install
$env:NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000"
npm run dev
```

Frontend URL:
[http://localhost:3000](http://localhost:3000)

## Important Note

If the frontend does not start because of Node.js version issues, install a newer Node.js version or use a frontend dependency set compatible with your machine.

## One-Line Summary For Stakeholders

"This dashboard helps pharma manufacturing teams detect process instability earlier, focus attention where it matters, and improve batch outcomes across the network."
