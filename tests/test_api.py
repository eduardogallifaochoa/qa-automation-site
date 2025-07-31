import sys
import os

# Add the parent directory to PYTHONPATH to import backend module correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app  # Import FastAPI app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_login_api_success():
    """Test login endpoint with valid credentials."""
    response = client.post("/api/login", json={"username": "admin", "password": "1234"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_login_api_failure():
    """Test login endpoint with invalid credentials."""
    response = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_contact_api_success():
    """Test contact endpoint with valid data."""
    data = {"name": "Eddie", "email": "eddie@mail.com", "message": "Hello from pytest!"}
    response = client.post("/api/contact", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Message received"}
