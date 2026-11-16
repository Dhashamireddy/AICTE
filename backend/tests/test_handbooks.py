def test_create_and_list_handbook(client):
    response = client.post("/api/handbooks", json={"edition_name": "Sample Edition (test)", "is_official": False})
    assert response.status_code == 201
    assert response.json()["is_official"] is False
    assert len(client.get("/api/handbooks").json()) == 1


def test_duplicate_handbook_edition_is_conflict(client):
    client.post("/api/handbooks", json={"edition_name": "Sample Edition (test)"})
    response = client.post("/api/handbooks", json={"edition_name": "Sample Edition (test)"})
    assert response.status_code == 409