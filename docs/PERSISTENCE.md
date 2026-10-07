# Astrovision Production Persistence & IDOR Security Architecture

## 1. Persistence Engine & Models (`apps/api/db/`)
Astrovision implements a production-grade relational persistence layer via SQLAlchemy ORM supporting SQLite persistent storage (default `astrovision.db` file) and PostgreSQL (`DATABASE_URL`).

### Persistent Models
- **`UserModel`** (`users` table): User accounts and authentication credentials.
- **`BirthProfileModel`** (`birth_profiles` table): User birth profile particulars (Name, DOB, Time, Location, IANA Timezone).
- **`CalculationReportModel`** (`calculation_reports` table): Persistent master evidence, prediction packages, and comprehensive report JSON artifacts.
- **`AIInterpretationRecordModel`** (`ai_interpretations` table): Historical domain AI narrative interpretations and validation statuses.
- **`SavedChartModel`** (`saved_charts` table): User saved natal charts and notes.
- **`AuditRecordModel`** (`audit_records` table): Server-side security audit logs for user actions.

## 2. Server-Enforced User Ownership & IDOR Protection
- **No Client-Supplied Owner Trust**: The server **never** trusts client-supplied user IDs in request bodies or URL path parameters. User identity is resolved strictly server-side via `get_current_user` dependency from the `X-User-Token` or `Authorization: Bearer` headers.
- **Server-Enforced Scope Filtering**: Every read, update, delete, or export operation filters strictly on `(Model.id == record_id) & (Model.user_id == current_user.id)`.
- **404 Not Found Handling**: If User B attempts to access User A's record, the server returns `HTTP 404 Not Found` (preventing resource existence enumeration).

## 3. Query Indexes
For ultra-fast query execution, explicit database indexes are defined on:
- `users.email`
- `birth_profiles.user_id` and compound index `(user_id, id)`
- `calculation_reports.user_id`, `birth_profile_id`, `chart_hash`
- `ai_interpretations.user_id`, `calculation_report_id`
- `saved_charts.user_id`, `birth_profile_id`

## 4. Setup & Migration Instructions
1. **Default Persistent SQLite Storage**:
   By default, the engine creates and connects to `./astrovision.db` automatically on startup via `init_db()`.
2. **PostgreSQL Migration**:
   To connect to a production PostgreSQL cluster, set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL="postgresql://astro_user:secure_password@localhost:5432/astrovision_db"
   ```
3. **Health Status Verification**:
   Query `GET /health`. It will report:
   ```json
   {
     "status": "healthy",
     "api_status": "active",
     "database_status": "sqlite_persistent"
   }
   ```
