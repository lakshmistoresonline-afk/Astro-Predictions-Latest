# Astrovision Endpoint Security & Authorization Matrix

## 1. Authorization Class Definitions
- **`public`**: Open endpoint accessible without authentication (e.g., server health checks, user signup/login).
- **`authenticated_user`**: Endpoint requiring a valid Bearer JWT access token (`Authorization: Bearer <token>`).
- **`owner_only`**: Endpoint requiring an authenticated user token AND server-side user ID filter (`Model.user_id == current_user.id`) for strict IDOR protection. Unowned queries return `HTTP 404 Not Found`.
- **`admin_only`**: Administrative route requiring `verify_admin_key` (`X-Admin-Key` or `Authorization: Bearer <admin_key>`). Returns `401` on missing credentials and `403` on invalid key.

## 2. Complete Endpoint Security Matrix

| Endpoint Route | HTTP Method | Authorization Scope | Authentication Requirement | IDOR Enforcement | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/health` | `GET` | `public` | None | N/A | System health, database, and ephemeris status |
| `/ready` | `GET` | `public` | None | N/A | DE440s ephemeris readiness check |
| `/version` | `GET` | `public` | None | N/A | Engine version and ayanamsha metadata |
| `/api/v1/auth/register` | `POST` | `public` | None | N/A | User account registration & token issuance |
| `/api/v1/auth/login` | `POST` | `public` | None | N/A | User authentication & token issuance |
| `/api/v1/auth/me` | `GET` | `authenticated_user` | Bearer JWT Token | Server-Enforced | Current authenticated user profile |
| `/api/v1/birth-profile` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Master evidence & prediction calculation |
| `/api/v1/transits` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Real-time planetary transits snapshot |
| `/api/v1/panchanga` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Local solar day Panchanga calculation |
| `/api/v1/muhurta` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Activity Muhurta precedence evaluations |
| `/api/v1/jaimini` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Jaimini Chara Karakas & Arudha Lagna |
| `/api/v1/timing-windows` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Convergent predictive timing windows |
| `/api/v1/interpret-evidence`| `POST` | `authenticated_user` | Bearer JWT Token | N/A | Server-owned evidence AI interpretation |
| `/api/v1/compatibility` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | 36-Point Vedic Ashtakoota matching |
| `/api/v1/rectification` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | Event-date birth time rectification |
| `/api/v1/export/pdf` | `POST` | `authenticated_user` | Bearer JWT Token | N/A | 12-Chapter PDF report treatise export |
| `/api/v1/profiles` | `POST` | `owner_only` | Bearer JWT Token | Server-Enforced | Create user-owned birth profile |
| `/api/v1/profiles` | `GET` | `owner_only` | Bearer JWT Token | Server-Enforced | List user's birth profiles |
| `/api/v1/profiles/{id}` | `GET` | `owner_only` | Bearer JWT Token | Server-Enforced | Get birth profile (404 if unowned) |
| `/api/v1/profiles/{id}` | `PUT` | `owner_only` | Bearer JWT Token | Server-Enforced | Update birth profile (404 if unowned) |
| `/api/v1/profiles/{id}` | `DELETE` | `owner_only` | Bearer JWT Token | Server-Enforced | Delete birth profile (404 if unowned) |
| `/api/v1/reports` | `POST` | `owner_only` | Bearer JWT Token | Server-Enforced | Calculate & save persistent report |
| `/api/v1/reports/{id}` | `GET` | `owner_only` | Bearer JWT Token | Server-Enforced | Get calculation report (404 if unowned) |
| `/api/v1/reports/{id}/pdf`| `GET` | `owner_only` | Bearer JWT Token | Server-Enforced | Export report PDF (404 if unowned) |
| `/api/v1/admin/stats` | `GET` | `admin_only` | Admin Key / Bearer | N/A | Server operational stats & versions |
