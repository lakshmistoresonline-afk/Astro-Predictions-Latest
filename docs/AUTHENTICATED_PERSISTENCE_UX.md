# Astrovision Authenticated Persistence & User Lifecycle Architecture

## 1. Authentication & Session Architecture
Astrovision strictly enforces server-side user context resolution on all persistent user resources. User passwords are stored using salted **PBKDF2-HMAC-SHA256** with $100,000$ iterations. Session authentication relies on HMAC-SHA256 signed **JWT Access Tokens** (`Authorization: Bearer <token>`).

## 2. Complete User Resource Lifecycle

```
[ User Registration / Login ] ── (POST /api/v1/auth/register or /login) ──► [ Bearer Access Token ]
                                                                                   │
   ┌───────────────────────────────────────────────────────────────────────────────┘
   │
   ├─► 1. Save Birth Profile ─────────► (POST /api/v1/profiles)
   ├─► 2. List Profiles ──────────────► (GET /api/v1/profiles)
   ├─► 3. Load / Recalculate Profile ─► (GET /api/v1/profiles/{id})
   ├─► 4. Calculate & Save Report ────► (POST /api/v1/reports?profile_id={id})
   ├─► 5. Browse Report History ──────► (GET /api/v1/reports/{id})
   ├─► 6. Export PDF Report ──────────► (GET /api/v1/reports/{id}/pdf)
   ├─► 7. Create Saved Chart & Notes ─► (POST /api/v1/saved-charts)
   └─► 8. Delete Profile / Saved Chart ─► (DELETE /api/v1/profiles/{id})
```

## 3. Server-Enforced IDOR Security & Scope Isolation
- **Server-Enforced Filtering**: Every database query filters strictly on `(Model.id == resource_id) & (Model.user_id == current_user.id)`.
- **404 Handling**: Unowned resource queries return `HTTP 404 Not Found`, preventing resource existence enumeration.
- **Client Credential Security**: Neither Web (`localStorage`) nor Android (`SharedPreferences`) stores plaintext passwords.
- **Expired Session Handling**: Requests with expired tokens fail closed with `HTTP 401 Unauthorized` (`"Access token has expired."`), directing clients to re-authenticate.
