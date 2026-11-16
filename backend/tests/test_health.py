from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_healthy():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["database"] == "connected"


def test_health_includes_disclaimer():
    body = client.get("/api/health").json()
    assert "not an official" in body["disclaimer"].lower()
