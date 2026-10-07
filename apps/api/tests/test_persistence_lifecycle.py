"""
Integration Test Suite for Complete Authenticated Persistence Lifecycle, Saved Charts & Reports, and IDOR Isolation.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_complete_persistence_lifecycle():
    """Verifies complete end-to-end user lifecycle across registration, profiles, reports, saved charts, PDF export, and IDOR isolation."""
    # Step 1: Register User A and User B
    res_a = client.post("/api/v1/auth/register", json={
        "email": "lifecycle_a@astrovision.test",
        "password": "Password123!",
        "full_name": "User Alpha"
    }).json()
    token_a = res_a["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    res_b = client.post("/api/v1/auth/register", json={
        "email": "lifecycle_b@astrovision.test",
        "password": "Password123!",
        "full_name": "User Beta"
    }).json()
    token_b = res_b["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Step 2: User A creates birth profile
    profile_a = client.post("/api/v1/profiles", json={
        "name": "Alpha Profile",
        "year": 1992, "month": 6, "day": 20,
        "hour": 15, "minute": 45, "second": 0,
        "timezone_str": "Asia/Kolkata",
        "latitude": 28.6139, "longitude": 77.2090,
        "place_name": "New Delhi", "country": "India"
    }, headers=headers_a).json()
    prof_id = profile_a["id"]

    # Step 3: User A lists profiles
    list_a = client.get("/api/v1/profiles", headers=headers_a).json()
    assert any(p["id"] == prof_id for p in list_a)

    # Step 4: User A calculates and saves report
    rep_res = client.post(f"/api/v1/reports?profile_id={prof_id}", headers=headers_a).json()
    report_id = rep_res["id"]

    # Step 5: User A retrieves report and exports PDF
    get_rep = client.get(f"/api/v1/reports/{report_id}", headers=headers_a)
    assert get_rep.status_code == 200
    assert "master_evidence" in get_rep.json()

    pdf_res = client.get(f"/api/v1/reports/{report_id}/pdf", headers=headers_a)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content.startswith(b"%PDF-")

    # Step 6: User A creates saved chart with title and notes
    chart_res = client.post("/api/v1/saved-charts", json={
        "birth_profile_id": prof_id,
        "chart_title": "My Natal Kundali",
        "notes": "Important Lagna and Vimshottari Dasha details"
    }, headers=headers_a).json()
    chart_id = chart_res["id"]

    charts_list = client.get("/api/v1/saved-charts", headers=headers_a).json()
    assert any(c["id"] == chart_id for c in charts_list)

    # Step 7: IDOR Checks - User B attempts to access User A's resources -> 404 Not Found
    assert client.get(f"/api/v1/profiles/{prof_id}", headers=headers_b).status_code == 404
    assert client.put(f"/api/v1/profiles/{prof_id}", json={
        "name": "Hacked", "year": 1992, "month": 6, "day": 20,
        "hour": 15, "minute": 45, "second": 0, "timezone_str": "Asia/Kolkata",
        "latitude": 28.6139, "longitude": 77.2090, "place_name": "New Delhi", "country": "India"
    }, headers=headers_b).status_code == 404
    assert client.get(f"/api/v1/reports/{report_id}", headers=headers_b).status_code == 404
    assert client.get(f"/api/v1/reports/{report_id}/pdf", headers=headers_b).status_code == 404
    assert client.delete(f"/api/v1/saved-charts/{chart_id}", headers=headers_b).status_code == 404

    # Step 8: User A deletes saved chart and birth profile
    del_chart = client.delete(f"/api/v1/saved-charts/{chart_id}", headers=headers_a)
    assert del_chart.status_code == 200

    del_prof = client.delete(f"/api/v1/profiles/{prof_id}", headers=headers_a)
    assert del_prof.status_code == 200
