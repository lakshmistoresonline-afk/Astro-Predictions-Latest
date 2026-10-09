"""
Test Suite for Gold Standard JSON Export and Celestial Dossier PDF Endpoints.
Verifies POST /api/v1/export/gold-standard-json and POST /api/v1/export/pdf dynamically over birth inputs.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.db.database import init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def get_auth_token(email: str = "gold_export_user@astrovision.test") -> str:
    res = client.post("/api/v1/auth/register", json={
        "email": email, "password": "Password123!", "full_name": "Gold Export User"
    })
    if res.status_code == 201:
        return res.json()["access_token"]
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
    return login.json()["access_token"]

def test_gold_standard_json_export_endpoint():
    """POST /api/v1/export/gold-standard-json must dynamically return the complete 30-section dossier structure."""
    token = get_auth_token()
    payload = {
        "name": "Subramanian T S",
        "year": 1986, "month": 9, "day": 28,
        "hour": 16, "minute": 30,
        "latitude": 10.7867, "longitude": 76.6548,
        "place_name": "Palakkad, Kerala", "country": "India",
        "timezone_str": "Asia/Kolkata"
    }

    res = client.post("/api/v1/export/gold-standard-json", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()

    assert data["title"] == "THE CELESTIAL DOSSIER"
    assert data["executive_summary"]["native_name"] == "Subramanian T S"
    assert data["executive_summary"]["anchor_metrics"]["ascendant"] == "Aquarius 12°40′"
    assert "Pushya" in data["executive_summary"]["anchor_metrics"]["moon"]
    assert len(data["sections"]["s02_planetary_ledger"]["table"]) >= 9

def test_celestial_dossier_pdf_export_endpoint():
    """POST /api/v1/export/pdf must dynamically return a publication-grade binary PDF starting with %PDF-1.4."""
    token = get_auth_token()
    payload = {
        "name": "Subramanian T S",
        "year": 1986, "month": 9, "day": 28,
        "hour": 16, "minute": 30,
        "latitude": 10.7867, "longitude": 76.6548,
        "place_name": "Palakkad, Kerala", "country": "India",
        "timezone_str": "Asia/Kolkata"
    }

    res = client.post("/api/v1/export/pdf", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert res.content.startswith(b"%PDF-")
    assert len(res.content) > 1000
