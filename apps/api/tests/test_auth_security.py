"""
Test Suite for Production User Authentication, Token Issuance, Password Hashing, and Security Controls.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_user_registration_creates_account_and_returns_token():
    """User registration must hash password and return signed JWT token."""
    payload = {
        "email": "user_reg_001@astrovision.test",
        "password": "SecurePassword123!",
        "full_name": "Test User One"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "user_reg_001@astrovision.test"
    assert data["user_id"] is not None

def test_user_registration_duplicate_email_conflict():
    """Duplicate email registration must return HTTP 409 Conflict."""
    payload = {
        "email": "user_dup@astrovision.test",
        "password": "SecurePassword123!",
        "full_name": "Duplicate User"
    }
    resp1 = client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 409
    assert "already exists" in resp2.json()["detail"]

def test_user_login_valid_credentials_returns_token():
    """User login with valid email/password returns signed JWT token."""
    reg_payload = {
        "email": "user_login_test@astrovision.test",
        "password": "MySecretPassword123",
        "full_name": "Login Test User"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": "user_login_test@astrovision.test",
        "password": "MySecretPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "user_login_test@astrovision.test"

def test_user_login_invalid_password_unauthorized():
    """User login with invalid password must return HTTP 401 Unauthorized."""
    login_payload = {
        "email": "user_login_test@astrovision.test",
        "password": "WrongPasswordAttempt"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_unauthenticated_request_to_protected_route_fails_401():
    """Unauthenticated request to protected endpoints must return HTTP 401."""
    response = client.get("/api/v1/profiles")
    assert response.status_code == 401
    assert "Missing authentication credentials" in response.json()["detail"]

def test_invalid_token_fails_401():
    """Request with invalid/malformed Bearer token must return HTTP 401."""
    headers = {"Authorization": "Bearer invalid_malformed_token_12345"}
    response = client.get("/api/v1/profiles", headers=headers)
    assert response.status_code == 401
    assert "Malformed access token" in response.json()["detail"]

def test_authenticated_user_profile_me_endpoint():
    """GET /api/v1/auth/me returns profile for current Bearer token."""
    reg_payload = {
        "email": "me_test@astrovision.test",
        "password": "MySecretPassword123",
        "full_name": "Me Profile User"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload).json()
    token = reg_res["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me_test@astrovision.test"
    assert data["full_name"] == "Me Profile User"

def test_user_a_cannot_access_user_b_resources():
    """IDOR Check: User B token cannot read or modify User A's birth profile."""
    # Register User A and create birth profile
    reg_a = client.post("/api/v1/auth/register", json={
        "email": "user_a_auth@astrovision.test", "password": "Password123!", "full_name": "User A"
    }).json()
    token_a = reg_a["access_token"]

    prof_res = client.post("/api/v1/profiles", json={
        "name": "User A Profile", "year": 1990, "month": 5, "day": 15,
        "hour": 14, "minute": 30, "timezone_str": "Asia/Kolkata",
        "latitude": 18.9220, "longitude": 72.8347, "place_name": "Mumbai", "country": "India"
    }, headers={"Authorization": f"Bearer {token_a}"}).json()
    prof_id = prof_res["id"]

    # Register User B
    reg_b = client.post("/api/v1/auth/register", json={
        "email": "user_b_auth@astrovision.test", "password": "Password123!", "full_name": "User B"
    }).json()
    token_b = reg_b["access_token"]

    # User B attempts to read User A profile -> 404 Not Found
    idor_read = client.get(f"/api/v1/profiles/{prof_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert idor_read.status_code == 404

    # User B attempts to delete User A profile -> 404 Not Found
    idor_delete = client.delete(f"/api/v1/profiles/{prof_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert idor_delete.status_code == 404
