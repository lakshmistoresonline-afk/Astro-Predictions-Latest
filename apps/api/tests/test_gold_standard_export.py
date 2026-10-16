"""
Test Suite for Gold Standard JSON Export and Celestial Dossier PDF Endpoints.
Verifies POST /api/v1/export/gold-standard-json and POST /api/v1/export/pdf dynamically over birth inputs with PDF text extraction.
"""
import io
import pytest
import pypdf
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
    assert len(data["sections_list"]) == 30

def test_celestial_dossier_pdf_export_endpoint_and_text_extraction():
    """POST /api/v1/export/pdf must dynamically return binary PDF bytes containing native birth details and 30 sections."""
    token = get_auth_token()
    payload_a = {
        "name": "Subramanian T S",
        "year": 1986, "month": 9, "day": 28,
        "hour": 16, "minute": 30,
        "latitude": 10.7867, "longitude": 76.6548,
        "place_name": "Palakkad, Kerala", "country": "India",
        "timezone_str": "Asia/Kolkata"
    }

    payload_b = {
        "name": "John Doe",
        "year": 1995, "month": 1, "day": 1,
        "hour": 12, "minute": 0,
        "latitude": 40.7128, "longitude": -74.0060,
        "place_name": "New York", "country": "United States",
        "timezone_str": "America/New_York"
    }

    # Test Profile A Export
    res_a = client.post("/api/v1/export/pdf", json=payload_a, headers={"Authorization": f"Bearer {token}"})
    assert res_a.status_code == 200
    assert res_a.headers["content-type"] == "application/pdf"
    assert res_a.content.startswith(b"%PDF-")

    text_a = "".join(page.extract_text() for page in pypdf.PdfReader(io.BytesIO(res_a.content)).pages)
    assert "SUBRAMANIAN T S" in text_a
    assert "1986-09-28" in text_a
    assert "Palakkad" in text_a

    # Test Profile B Export
    res_b = client.post("/api/v1/export/pdf", json=payload_b, headers={"Authorization": f"Bearer {token}"})
    assert res_b.status_code == 200
    assert res_b.headers["content-type"] == "application/pdf"
    assert res_b.content.startswith(b"%PDF-")

    text_b = "".join(page.extract_text() for page in pypdf.PdfReader(io.BytesIO(res_b.content)).pages)
    assert "JOHN DOE" in text_b
    assert "1995-01-01" in text_b
    assert "New York" in text_b

    # Verify Profile Isolation (No Data Leakage)
    assert res_a.content != res_b.content
    assert "SUBRAMANIAN T S" not in text_b
    assert "JOHN DOE" not in text_a
