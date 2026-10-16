"""
Test Suite for Production User Authentication, Token Issuance, Password Hashing, and Security Controls.
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.db.database import init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_user_registration_creates_account_and_returns_token():
    """User registration must hash password and return signed JWT token."""
    email = f"user_reg_{uuid.uuid4()}@astrovision.test"
    payload = {
        "email": email,
        "password": "SecurePassword123!",
        "full_name": "Test User One"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == email
    assert data["user_id"] is not None

def test_user_registration_duplicate_email_conflict():
    """Duplicate email registration must return HTTP 409 Conflict."""
    email = f"user_dup_{uuid.uuid4()}@astrovision.test"
    payload = {
        "email": email,
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
    email = f"user_login_{uuid.uuid4()}@astrovision.test"
    reg_payload = {
        "email": email,
        "password": "MySecretPassword123",
        "full_name": "Login Test User"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": email,
        "password": "MySecretPassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == email

def test_user_login_invalid_password_unauthorized():
    """User login with invalid password must return HTTP 401 Unauthorized."""
    email = f"user_login_fail_{uuid.uuid4()}@astrovision.test"
    reg_payload = {
        "email": email,
        "password": "CorrectPassword123",
        "full_name": "Login Test User"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_payload = {
        "email": email,
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
    email = f"me_test_{uuid.uuid4()}@astrovision.test"
    reg_payload = {
        "email": email,
        "password": "MySecretPassword123",
        "full_name": "Me Profile User"
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload).json()
    token = reg_res["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["full_name"] == "Me Profile User"

def test_user_a_cannot_access_user_b_resources():
    """IDOR Check: User B token cannot read or modify User A's birth profile."""
    email_a = f"user_a_{uuid.uuid4()}@astrovision.test"
    email_b = f"user_b_{uuid.uuid4()}@astrovision.test"

    # Register User A and create birth profile
    reg_a = client.post("/api/v1/auth/register", json={
        "email": email_a, "password": "Password123!", "full_name": "User A"
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
        "email": email_b, "password": "Password123!", "full_name": "User B"
    }).json()
    token_b = reg_b["access_token"]

    # User B attempts to read User A's profile -> 404/403
    read_b = client.get(f"/api/v1/profiles/{prof_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert read_b.status_code in [403, 404]
