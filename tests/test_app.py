
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_valid_email(client):
    response = client.post(
        "/validate",
        json={"email": "security@verify-account123.com"}
    )

    assert response.status_code == 200
    assert response.json["risk_score"] == 45
    assert response.json["risk_level"] == "Medium"


def test_invalid_email(client):
    response = client.post(
        "/validate",
        json={"email": "invalid-email"}
    )

    assert response.status_code == 200
    assert response.json["risk_level"] == "Invalid"


def test_missing_email(client):
    response = client.post("/validate", json={})

    assert response.status_code == 400


def test_history(client):
    response = client.get("/history")

    assert response.status_code == 200
    assert "history" in response.json
    assert "total" in response.json

