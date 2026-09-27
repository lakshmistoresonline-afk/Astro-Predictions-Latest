# Astrovision Baseline Audit

## 1. Repository Snapshot
- **HEAD Commit SHA**: `79a83f9` (Main branch)
- **Repository Tree**: Monorepo with `apps/api` (FastAPI backend), `apps/web` (Next.js frontend), and `docs/` (technical audits).
- **Python Dependencies**: FastAPI, Pydantic, NumPy, Uvicorn, Pytest, Pytz, Requests.
- **Frontend Dependencies**: Next.js 14, React, Tailwind CSS.
- **Test Suite**: Pytest configured in `apps/api/tests/`.

## 2. Baseline Architecture
- Deterministic astrological computation engine powered by high-precision astronomical Meeus algorithms and Vedic/Western rule sets.
- Strict isolation between user birth profiles and calculation snapshots.
