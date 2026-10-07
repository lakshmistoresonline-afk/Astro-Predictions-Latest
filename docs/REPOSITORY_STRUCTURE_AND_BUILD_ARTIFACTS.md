# Astrovision Repository Structure & Build Artifacts Specification

## 1. Directory Separation & Ownership
The repository enforces strict separation between source code, test suites, immutable reference data, and generated build/certification artifacts:

| Category | Directory / File Path | Description | Version Control Policy |
| :--- | :--- | :--- | :--- |
| **Backend Source** | `apps/api/` | FastAPI routes, calculation engines, database models | **TRACKED IN GIT** |
| **Frontend Source** | `apps/web/` | Next.js 14 Jetpack-inspired web client & components | **TRACKED IN GIT** |
| **Android Source** | `app/` | Jetpack Compose Android client & Kotlin ViewModels | **TRACKED IN GIT** |
| **Test Suites** | `apps/api/tests/` | Pytest unit, integration, IDOR & contract test cases | **TRACKED IN GIT** |
| **Immutable Fixtures**| `apps/api/tests/fixtures/`, `reference_source/` | Frozen reference data & golden test fixtures | **TRACKED IN GIT** |
| **Documentation** | `docs/` | Architecture specs, API contracts, security audits | **TRACKED IN GIT** |
| **Certification** | `reports/`, `scripts/` | Certification reports (`release_certification_report.md`) | **TRACKED IN GIT** |
| **Build Artifacts** | `.gradle/`, `app/build/`, `.next/`, `node_modules/` | Local compilation caches and dependencies | **IGNORED (.gitignore)** |
| **Local Environment**| `local.properties`, `.env`, `astrovision.db` | Local Android SDK paths, secrets, local SQLite DB | **IGNORED (.gitignore)** |

## 2. Regeneration Instructions for Generated Artifacts
1. **Android Build & APK**:
   ```bash
   ./gradlew app:assembleDebug
   ```
2. **Web Build (`apps/web`)**:
   ```bash
   cd apps/web && npm run build
   ```
3. **Release Certification Report**:
   ```bash
   python scripts/run_release_certification.py
   ```
4. **OpenAPI Specification**:
   Served live at `http://localhost:8000/openapi.json`.
