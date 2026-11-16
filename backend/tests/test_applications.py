def valid_payload(**overrides):
    payload = {
        "institution": {
            "name": "Sample Institute of Technology",
            "institution_type": "private_self_financing",
            "state": "Karnataka",
            "city": "Bengaluru",
            "has_existing_aicte_approval": True,
        },
        "proposed_course": "Computer Science and Engineering",
        "course_level": "undergraduate",
        "category": "new_course",
        "proposed_intake": 60,
        "infrastructure_details": {"classrooms": 10, "laboratories": 4, "faculty_count": 20},
    }
    payload.update(overrides)
    return payload


def test_create_application_success(client):
    response = client.post("/api/applications", json=valid_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["status"] == "draft"
    assert body["institution"]["name"] == "Sample Institute of Technology"
    assert body["infrastructure_details"]["laboratories"] == 4


def test_get_application_by_id(client):
    created = client.post("/api/applications", json=valid_payload()).json()
    response = client.get(f"/api/applications/{created['id']}")
    assert response.status_code == 200
    assert response.json()["proposed_course"] == "Computer Science and Engineering"


def test_get_missing_application_returns_404(client):
    response = client.get("/api/applications/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_list_applications_newest_first(client):
    client.post("/api/applications", json=valid_payload())
    client.post("/api/applications", json=valid_payload(proposed_course="Mechanical Engineering"))
    response = client.get("/api/applications")
    assert response.status_code == 200
    courses = [a["proposed_course"] for a in response.json()]
    assert courses == ["Mechanical Engineering", "Computer Science and Engineering"]


def test_rejects_zero_intake(client):
    response = client.post("/api/applications", json=valid_payload(proposed_intake=0))
    assert response.status_code == 422


def test_rejects_invalid_course_level(client):
    response = client.post("/api/applications", json=valid_payload(course_level="phd-ish"))
    assert response.status_code == 422


def test_rejects_invalid_institution_type(client):
    bad = valid_payload()
    bad["institution"]["institution_type"] = "spaceship"
    assert client.post("/api/applications", json=bad).status_code == 422


def test_rejects_blank_name(client):
    bad = valid_payload()
    bad["institution"]["name"] = "     "
    assert client.post("/api/applications", json=bad).status_code == 422


def test_rejects_negative_infrastructure(client):
    bad = valid_payload(infrastructure_details={"classrooms": -3})
    assert client.post("/api/applications", json=bad).status_code == 422


def test_unknown_handbook_returns_404_and_saves_nothing(client):
    response = client.post("/api/applications", json=valid_payload(handbook_source_id=42))
    assert response.status_code == 404
    assert client.get("/api/applications").json() == []


def test_application_with_valid_handbook(client):
    hb = client.post("/api/handbooks", json={"edition_name": "Sample Edition (test)"}).json()
    response = client.post("/api/applications", json=valid_payload(handbook_source_id=hb["id"]))
    assert response.status_code == 201
    assert response.json()["handbook_source_id"] == hb["id"]