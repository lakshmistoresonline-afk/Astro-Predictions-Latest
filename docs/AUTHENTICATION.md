# Astrovision Production Authentication & Security Architecture

## 1. Authentication Engine & Cryptographic Design
Astrovision implements a production-grade, zero-trust authentication architecture backed by salted PBKDF2-HMAC-SHA256 password hashing and cryptographically signed JWT access tokens.

### Password Hashing (`apps/api/db/auth.py`)
- **Algorithm**: PBKDF2-HMAC-SHA256 with $100,000$ iterations.
- **Salt**: 16-byte cryptographically secure random salt (`secrets.token_bytes(16)`) generated per user account and stored alongside the password hash in `users.password_salt`.
- **Verification**: Uses constant-time comparison via Python `secrets.compare_digest` to prevent timing attacks.

### Access Token Specification (`apps/api/db/auth.py`)
- **Format**: HMAC-SHA256 signed 3-part JSON Web Token (`header.payload.signature`).
- **Claims**:
  - `sub`: Authenticated User ID (UUID)
  - `email`: User's registered email
  - `iat`: Issued-at Unix timestamp
  - `exp`: Expiration Unix timestamp ($24\text{ hours}$ default)
- **Signature Verification**: Validates signature using `settings.jwt_secret_key` and asserts `now < exp`.

## 2. Server-Enforced User Context & IDOR Security
- **Fail-Closed Authentication**: Unauthenticated requests to protected endpoints return `HTTP 401 Unauthorized`. Zero fail-open public user fallbacks! Zero user creation from arbitrary token strings!
- **Server-Owned Identity Resolution**: `get_current_user` extracts `user_id` strictly from the verified JWT `sub` claim. Client-supplied user IDs, emails, or `X-User-Token` strings in request bodies or path parameters are **never** trusted for identity resolution.
- **Ownership Scope Filtering**: All CRUD routes filter strictly on `(Model.id == resource_id) & (Model.user_id == current_user.id)`. Unowned or unauthorized queries return `HTTP 404 Not Found`.

## 3. Authentication API Endpoints (`/api/v1/auth/*`)
1. `POST /api/v1/auth/register`:
   Registers a new user account with salted PBKDF2 password hashing and issues an access token.
2. `POST /api/v1/auth/login`:
   Authenticates user credentials and issues a signed JWT access token.
3. `GET /api/v1/auth/me`:
   Returns profile information for the authenticated user token context.

## 4. Client Integration (Web & Android)
- **Header**: Pass `Authorization: Bearer <access_token>` on all requests.
- **Web Client**: Set `setAuthToken(token)` in `apps/web/services/apiClient.ts`.
- **Android Client**: Set `setAuthToken(token)` in `AstrovisionRepository.kt`.
