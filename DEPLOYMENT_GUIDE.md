# Deployment Guide

## Goal

Publish the prototype so anyone with a link can open it in a browser.

Recommended setup:

- Backend API on Render
- Frontend dashboard on Vercel

## What You Need

- a GitHub account
- a Render account
- a Vercel account
- this project folder uploaded to a GitHub repository

## Deployment Order

1. Put the code on GitHub
2. Deploy the backend on Render
3. Copy the Render backend URL
4. Deploy the frontend on Vercel
5. Add the backend URL as an environment variable in Vercel
6. Share the Vercel frontend URL

## Backend Settings

The backend is preconfigured in `render.yaml`.

Render will use:

- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

The repo pins Python in `.python-version` so Render uses Python 3.11 instead of the newer default Python 3.14.x that may break package installs.

## Frontend Settings

When deploying on Vercel, set:

- Root Directory: `frontend`
- Environment Variable:
  - `NEXT_PUBLIC_API_BASE_URL` = your Render backend URL

Example:

`NEXT_PUBLIC_API_BASE_URL=https://your-render-service.onrender.com`

## After Deployment

Share only the Vercel URL with business users.

Example:

`https://pharma-osd-control-tower.vercel.app`

That URL will load the frontend, which then calls the Render backend in the background.
