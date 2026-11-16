def test_health_returns_healthy(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["database"] == "connected"


def test_health_includes_disclaimer(client):
    body = client.get("/api/health").json()
    assert "not an official" in body["disclaimer"].lower()