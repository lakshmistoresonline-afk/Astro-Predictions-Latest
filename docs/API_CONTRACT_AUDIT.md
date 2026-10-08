# Astrovision Version 6.0.0 API Contract Audit Report

## Contract Synchronization Verification
Every backend FastAPI Pydantic schema, web TypeScript interface, and Android Retrofit model has been audited and synchronized across all endpoints.

### Key Endpoint Contracts

1. **`/api/v1/auth/register` & `/api/v1/auth/login`**:
   - **Request**: `UserRegisterRequest` (`email`, `password`, `full_name`) / `UserLoginRequest` (`email`, `password`).
   - **Response**: `TokenResponse` (`access_token`, `token_type`, `expires_in_hours`, `user_id`, `email`, `full_name`).
   - **Security**: Salted PBKDF2-HMAC-SHA256 password hashing (100,000 iterations).

2. **`/api/v1/auth/logout`**:
   - **Auth**: `Authorization: Bearer <token>`
   - **Response**: `{"status": "logged_out", "message": "Successfully logged out and session token revoked."}`
   - **Security**: Registers token SHA-256 digest in revocation registry `REVOKED_TOKEN_HASHES`.

3. **`/api/v1/birth-profile`**:
   - **Request**: `BirthProfileRequest` (`name`, `year`, `month`, `day`, `hour`, `minute`, `second`, `timezone_str`, `latitude`, `longitude`, `place_name`, `country`).
   - **Response**: `BirthProfileResponse` (`status`, `birth_input`, `master_evidence`, `predictions`, `svg_chart`, `report`).
   - **Evidence Integrity**: Includes 100% immutable `master_evidence_hash` (SHA-256).

4. **`/api/v1/export/pdf`**:
   - **Auth**: `Authorization: Bearer <token>`
   - **Response**: `application/pdf` binary stream starting with `%PDF-1.4`.
   - **Content**: 12-Chapter complete astrological treatise derived from deterministic evidence.
