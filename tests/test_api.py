import pytest
from fastapi.testclient import TestClient
from backend.app import app  # Adjust import if needed

client = TestClient(app)

def test_login_api_success():
    """
    Test successful login with valid credentials.
    """
    response = client.post("/api/login", json={"username": "admin", "password": "1234"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_api_failure():
    """
    Test login failure with invalid password.
    """
    response = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_contact_api_success():
    """
    Test successful contact form submission.
    """
    data = {"name": "Eddie", "email": "eddie@mail.com", "message": "Hello from pytest!"}
    response = client.post("/api/contact", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Message received"}  # Match backend response
