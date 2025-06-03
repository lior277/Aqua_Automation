import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.services.user_service import get_user_service

client = TestClient(app)

AUTH_HEADERS = {
    "Authorization": "Basic dGVzdHVzZXI6czNjcmV0"
}


@pytest.fixture(autouse=True)
def clear_fake_db():
    service = get_user_service()
    service.clear_all()
    yield


def test_health_check_no_auth():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["service"] == "aqua-api"


def test_create_user_without_auth():
    payload = {
        "israel_id": "123456789",
        "name": "John Doe",
        "phone_number": "+972501234567",
        "address": "1 Test St"
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 401


def test_create_user_with_wrong_auth():
    payload = {
        "israel_id": "123456789",
        "name": "John Doe",
        "phone_number": "+972501234567",
        "address": "1 Test St"
    }
    wrong_auth = {"Authorization": "Basic d3Jvbmc6Y3JlZHM="}  # wrong:creds
    resp = client.post("/users", json=payload, headers=wrong_auth)
    assert resp.status_code == 401


def test_create_user_with_valid_auth():
    payload = {
        "israel_id": "123456789",
        "name": "John Doe",
        "phone_number": "+972501234567",
        "address": "1 Test St"
    }
    resp = client.post("/users", json=payload, headers=AUTH_HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"] == 1
    assert data["israel_id"] == payload["israel_id"]
    assert data["name"] == payload["name"]


def test_get_user_requires_auth():
    resp = client.get("/users/1")
    assert resp.status_code == 401


def test_list_users_requires_auth():
    resp = client.get("/users")
    assert resp.status_code == 401


def test_full_flow_with_auth():
    payload = {
        "israel_id": "987654321",
        "name": "Test User",
        "phone_number": "+972501234567",
        "address": "Test Address"
    }
    create_resp = client.post("/users", json=payload, headers=AUTH_HEADERS)
    assert create_resp.status_code == 201
    user_id = create_resp.json()["user_id"]

    get_resp = client.get(f"/users/{user_id}", headers=AUTH_HEADERS)
    assert get_resp.status_code == 200
    assert get_resp.json()["israel_id"] == "987654321"

    list_resp = client.get("/users", headers=AUTH_HEADERS)
    assert list_resp.status_code == 200
    assert user_id in list_resp.json()


def test_duplicate_israeli_id():
    payload = {
        "israel_id": "111111111",
        "name": "First User",
        "phone_number": "+972501234567",
        "address": "Address 1"
    }

    resp1 = client.post("/users", json=payload, headers=AUTH_HEADERS)
    assert resp1.status_code == 201

    payload["name"] = "Second User"
    resp2 = client.post("/users", json=payload, headers=AUTH_HEADERS)
    assert resp2.status_code == 409
    assert "already exists" in resp2.json()["detail"]


def test_get_nonexistent_user():
    resp = client.get("/users/999", headers=AUTH_HEADERS)
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]
