# Astrovision Database Schema Migration & Alembic Guide

## 1. Migration Architecture
Astrovision uses **Alembic** as its deterministic database migration framework. Migration scripts in `alembic/versions/` govern schema upgrades and downgrades across SQLite and PostgreSQL databases.

## 2. Running Migrations

### Apply Migrations to Current Head
To upgrade the database schema to the latest version:
```bash
alembic upgrade head
```

### Rollback Migration One Step
To downgrade the database schema by one revision:
```bash
alembic downgrade -1
```

### Create a New Schema Migration
When modifying ORM models in `apps/api/db/models.py`:
```bash
alembic revision --autogenerate -m "describe_schema_changes"
```

## 3. Production Deployment Guidelines
1. In production environments (`ENVIRONMENT=production`), database migrations must be applied before starting the FastAPI server process:
   ```bash
   alembic upgrade head && uvicorn apps.api.main:app --host 0.0.0.0 --port 8000
   ```
2. The server calls `init_db()` at startup to ensure all tables exist on fresh database deployments.
