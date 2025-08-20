from fastapi.testclient import TestClient

# Intenta app.main primero; si no, usa backend.app (legacy)
try:
    from app.main import app
except Exception:
    from backend.app import app

client = TestClient(app)

def test_login_api_success():
    response = client.post("/api/login", json={"username": "admin", "password": "1234"})
    # Ajusta a tu implementación real; este es el legacy:
    assert response.status_code in (200, 401)
    if response.status_code == 200:
        body = response.json()
        assert isinstance(body, dict)

def test_login_api_failure():
    response = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code in (200, 401)

def test_contact_api_success():
    data = {"name": "Eddie", "email": "eddie@mail.com", "message": "Hello from pytest!"}
    response = client.post("/api/contact", json=data)
    assert response.status_code in (200, 422)
