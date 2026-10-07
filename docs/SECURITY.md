# Astrovision Administrative & Endpoint Security Architecture

## 1. Administrative Server-Side Authentication
Administrative API routes under `/api/v1/admin/` require server-side key verification via the `verify_admin_key` FastAPI dependency (`apps/api/routers/admin_export.py`).

### Headers Supported
- `X-Admin-Key: <ADMIN_API_KEY>`
- `Authorization: Bearer <ADMIN_API_KEY>`

### Credentials Resolution & Environment Configuration
Administrative credentials are read server-side from environment variables:
1. `ADMIN_API_KEY` (Environment override)
2. `settings.admin_api_key` (Configured default in `apps/api/config.py`)

No credentials are hardcoded or exposed in client bundles.

### Failure Responses
- **Missing Credentials**: Returns `HTTP 401 Unauthorized` with `WWW-Authenticate: Bearer` header.
- **Invalid Credentials**: Returns `HTTP 403 Forbidden`.
- **Timing Attack Prevention**: Uses constant-time comparison via Python `secrets.compare_digest(token, admin_key)`.

### Audit Logging
Administrative authentication attempts are logged via `astrovision.security` logger:
- Warnings logged for missing or invalid attempts (without logging secret keys).
- Informational logs recorded for authorized administrative access.

## 2. Endpoint Authorization Scopes
- **`/api/v1/admin/*`**: Admin-only routes requiring `verify_admin_key`.
- **`/api/v1/birth-profile`**, **`/api/v1/compatibility`**, **`/api/v1/rectification`**, **`/api/v1/export/pdf`**: Public / user-scoped calculation and export endpoints. Input validation enforced via Pydantic models with strict IANA timezone verification.
