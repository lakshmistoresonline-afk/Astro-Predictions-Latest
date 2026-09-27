import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health_and_version():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

    response = client.get("/version")
    assert response.status_code == 200
    version_data = response.json()
    assert "version" in version_data
    assert "engine_version" in version_data
