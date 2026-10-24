import app as app_module


def test_health_endpoint():
    client = app_module.app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_valid_email(monkeypatch):
    client = app_module.app.test_client()

    monkeypatch.setattr(
        app_module,
        "generate_explanation",
        lambda email, assessment: ("Test explanation", False),
    )

    response = client.post(
        "/validate",
        json={"email": "test@example.com"},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["valid_format"] is True
    assert data["risk_level"] == "Low"


def test_invalid_email_format(monkeypatch):
    client = app_module.app.test_client()

    monkeypatch.setattr(
        app_module,
        "generate_explanation",
        lambda email, assessment: ("Test explanation", False),
    )

    response = client.post(
        "/validate",
        json={"email": "not-an-email"},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["valid_format"] is False
    assert data["risk_level"] == "Invalid"


def test_missing_email():
    client = app_module.app.test_client()
    response = client.post("/validate", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_history_endpoint():
    client = app_module.app.test_client()
    response = client.get("/history")

    assert response.status_code == 200
    assert "results" in response.get_json()
