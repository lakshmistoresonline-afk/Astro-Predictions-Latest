# Astrovision Production Persistence Strategy & Database Architecture

## 1. Environment-Dependent Database Strategy
Astrovision strictly separates development/testing storage from production persistence:

- **Local Development & Testing (`ENVIRONMENT=development`)**:
  Uses SQLite file database (`sqlite:///./astrovision.db`). Enables rapid local development and isolated test runs.
- **Production (`ENVIRONMENT=production`)**:
  **Requires PostgreSQL**. The server startup validation (`validate_and_init_secrets()`) **refuses to start** (`RuntimeError`) if `ENVIRONMENT=production` and `DATABASE_URL` is missing or uses local SQLite (`sqlite://`).

## 2. Production Startup Validation
At server startup:
```python
if env == "production":
    if not db_url or db_url.strip().startswith("sqlite"):
        raise RuntimeError(
            "CRITICAL PERSISTENCE ERROR: Production deployment refused! "
            "DATABASE_URL environment variable is missing or configured for local SQLite (sqlite://). "
            "Production deployment requires a persistent PostgreSQL database connection string."
        )
```

## 3. Database Connection Pooling & Concurrency
When connected to a PostgreSQL database, SQLAlchemy configures production connection pooling:
- `pool_size = 10`
- `max_overflow = 20`
- `pool_timeout = 30`
- `pool_pre_ping = True`

This supports high concurrent user requests without connection exhaustion or stale connection drops.

## 4. Persistent Relational Models (`apps/api/db/models.py`)
- **`UserModel`** (`users` table): User account credentials with PBKDF2-HMAC-SHA256 salted password hashes and UUID primary keys.
- **`BirthProfileModel`** (`birth_profiles` table): User birth profile particulars with compound user index `(user_id, id)`.
- **`CalculationReportModel`** (`calculation_reports` table): Persistent master evidence, prediction packages, and report JSON artifacts.
- **`AIInterpretationRecordModel`** (`ai_interpretations` table): Historical domain AI narrative interpretations and validation statuses.
- **`SavedChartModel`** (`saved_charts` table): User saved natal charts and notes.
- **`AuditRecordModel`** (`audit_records` table): Server-side security audit logs for user operations.

## 5. Schema Migrations (Alembic)
Production schema upgrades are governed deterministically by Alembic:
```bash
alembic upgrade head
```
See [`docs/DATABASE_MIGRATIONS.md`](./DATABASE_MIGRATIONS.md) for full migration procedures.
