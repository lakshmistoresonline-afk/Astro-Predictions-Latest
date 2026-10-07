# Astrovision Secret Management, Rotation & CI Scanning Architecture

## 1. Zero Hardcoded Secrets Policy
Astrovision strictly enforces a zero-hardcoded-secrets policy across source code, configuration files, Docker Compose specifications, and deployment manifests.

### Production Startup Validation (`apps/api/config.py`)
At server startup (`validate_and_init_secrets()`), when `ENVIRONMENT=production`:
- The server **refuses to start** (`RuntimeError`) if `ADMIN_API_KEY` or `JWT_SECRET_KEY` is missing, set to a known default/demo string, or fewer than 16 characters.
- In development/testing (`ENVIRONMENT=development`), process-bound ephemeral random keys (`dev_admin_key_...`, `dev_jwt_key_...`) are generated dynamically if not set.

## 2. Environment Variable & Container Secret Injection
- **Docker Compose (`docker-compose.yml`)**: Uses environment variable interpolation `${ADMIN_API_KEY}` and `${JWT_SECRET_KEY}` read from local `.env` files or host environment (never static strings!).
- **Render (`render.yaml`)**: Uses platform-managed generated secret values (`generateValue: true`).
- **`.env.example`**: Contains placeholder strings only (`change_me_production_admin_secret_key_12345`).

## 3. Secret Rotation Procedure
In the event of key rotation or security maintenance:
1. **`ADMIN_API_KEY` Rotation**:
   Update `ADMIN_API_KEY` in environment variables or container deployment configuration. Restart the FastAPI server. Old admin keys are immediately invalidated via constant-time comparison (`secrets.compare_digest`).
2. **`JWT_SECRET_KEY` Rotation**:
   Update `JWT_SECRET_KEY` in environment variables. Restart the FastAPI server. Previously issued access tokens signed with the old secret key will automatically fail cryptographic signature verification (`HTTP 401 Unauthorized`), requiring users to log in again.

## 4. Secret Scanning in CI
Run the repository secret scanning check:
```bash
python scripts/scan_secrets.py
```
This script scans all python, typescript, kotlin, yaml, json, and markdown files to ensure zero static production credentials or hardcoded keys exist in source control.
