"""
Test Suite for JWT Hardening, Algorithm Enforcement, Token Revocation, and Logout Security.
"""
import pytest
import json
import base64
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings
from apps.api.db.database import init_db
from apps.api.db.auth import create_access_token, decode_access_token, _b64_url_encode
from apps.api.exceptions import AuthenticationError

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def get_auth_token(email: str = "jwt_hard_user@astrovision.test") -> str:
    res = client.post("/api/v1/auth/register", json={
        "email": email, "password": "Password123!", "full_name": "JWT Hardened User"
    })
    if res.status_code == 201:
        return res.json()["access_token"]
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return login.json()["access_token"]

def test_jwt_tampered_signature_rejected():
    """Tampered JWT signature MUST return HTTP 401 Unauthorized."""
    valid_token = get_auth_token()
    header, payload, sig = valid_token.split(".")

    # Tamper with signature
    tampered = f"{header}.{payload}.invalid_tampered_signature_12345"

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered}"})
    assert response.status_code == 401
    assert "Invalid access token cryptographic signature" in response.json()["detail"]

def test_jwt_altered_algorithm_none_rejected():
    """Altered JWT header algorithm ('alg': 'none') MUST be rejected with HTTP 401."""
    header_none = _b64_url_encode(json.dumps({"alg": "none", "typ": "JWT"}).encode("utf-8"))
    payload_valid = _b64_url_encode(json.dumps({"sub": "user_123", "exp": 9999999999}).encode("utf-8"))
    fake_token = f"{header_none}.{payload_valid}.fakesig"

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {fake_token}"})
    assert response.status_code == 401
    assert "Unsupported JWT algorithm" in response.json()["detail"]

def test_jwt_expired_token_rejected():
    """Expired JWT token (negative expiration delta) MUST return HTTP 401."""
    expired_token = create_access_token("user_expired_001", "expired@test.com", expires_delta_hours=-5)

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert "Access token has expired" in response.json()["detail"]

def test_jwt_token_revocation_logout():
    """Calling POST /api/v1/auth/logout revokes the token; subsequent requests return 401."""
    token = get_auth_token("logout_test_user@astrovision.test")
    headers = {"Authorization": f"Bearer {token}"}

    # Profile request succeeds before logout
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 200

    # User logs out
    logout_res = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_res.status_code == 200
    assert logout_res.json()["status"] == "logged_out"

    # Subsequent request with revoked token fails with 401
    replayed_res = client.get("/api/v1/auth/me", headers=headers)
    assert replayed_res.status_code == 401
    assert "revoked or logged out" in replayed_res.json()["detail"]
