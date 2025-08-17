# tests/api/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_login_ok():
    r = client.post("/api/login", json={"username": "u", "password": "p"})
    assert r.status_code == 200
    data = r.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_validation_error():
    # Missing required field -> 422
    r = client.post("/api/login", json={"username": "only-user"})
    assert r.status_code == 422


def test_contact_ok():
    r = client.post(
        "/api/contact",
        json={"name": "John", "email": "john@example.com", "message": "Hi"},
    )
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_security_headers_on_openapi():
    r = client.get("/openapi.json")
    # Presence, not exact match
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("cross-origin-opener-policy") == "same-origin"
    assert r.headers.get("cross-origin-embedder-policy") == "require-corp"
    assert r.headers.get("cross-origin-resource-policy") == "same-origin"
    # No-store to reduce ZAP "storable" warnings in dev
    assert "no-store" in (r.headers.get("cache-control") or "").lower()


def test_sitemap_xml():
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/xml")
    assert "no-store" in r.headers.get("cache-control", "").lower()
    assert "<urlset" in r.text
