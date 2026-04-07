# tests/api/test_get_endpoints.py
"""
Comprehensive GET endpoint tests for the QA Automation API.

Endpoints under test:
  GET /          → root (not in schema) → 200, JSON message
  GET /health    → liveness probe       → 200, {"status": "ok"}
  GET /sitemap.xml → sitemap            → 200, application/xml, valid XML
  GET /openapi.json → OpenAPI spec      → 200, valid JSON schema structure
  GET /docs      → Swagger UI           → 200, HTML
  GET /redoc     → ReDoc UI             → 200, HTML

Coverage areas per endpoint:
  - Status code
  - Response body shape / content
  - Content-Type header
  - Security headers (X-Content-Type-Options, COOP, COEP, CORP, Cache-Control)
  - Edge cases: trailing slash, wrong method (405), unknown routes (404)
  - Idempotency: same result on repeated calls
  - Response time (soft assertion via elapsed)
"""

import time
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SECURITY_HEADERS = {
    "x-content-type-options": "nosniff",
    "cross-origin-opener-policy": "same-origin",
    "cross-origin-embedder-policy": "require-corp",
    "cross-origin-resource-policy": "same-origin",
}


def assert_security_headers(response):
    """Assert that all expected security headers are present with correct values."""
    for header, expected_value in SECURITY_HEADERS.items():
        actual = response.headers.get(header)
        assert actual == expected_value, (
            f"Header '{header}': expected '{expected_value}', got '{actual}'"
        )
    cache = response.headers.get("cache-control", "")
    assert "no-store" in cache.lower(), (
        f"Expected 'no-store' in Cache-Control, got: '{cache}'"
    )


def assert_fast_response(response, max_seconds: float = 2.0):
    """Soft-assert that the response arrived within max_seconds."""
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Response took {elapsed:.3f}s — expected < {max_seconds}s"
    )


# ===========================================================================
# GET /  (root)
# ===========================================================================

class TestRoot:
    """Tests for GET / (root endpoint, not in OpenAPI schema)."""

    def test_status_200(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_response_is_json(self):
        r = client.get("/")
        assert r.headers.get("content-type", "").startswith("application/json")

    def test_response_body_has_message_key(self):
        r = client.get("/")
        body = r.json()
        assert "message" in body, f"Expected 'message' key in body, got: {body}"

    def test_response_message_is_string(self):
        r = client.get("/")
        assert isinstance(r.json()["message"], str)

    def test_response_message_not_empty(self):
        r = client.get("/")
        assert r.json()["message"].strip() != ""

    def test_security_headers(self):
        r = client.get("/")
        assert_security_headers(r)

    def test_idempotent(self):
        r1 = client.get("/")
        r2 = client.get("/")
        assert r1.status_code == r2.status_code
        assert r1.json() == r2.json()

    def test_response_time(self):
        r = client.get("/")
        assert_fast_response(r)

    def test_post_method_not_allowed(self):
        """POST / should return 405 Method Not Allowed."""
        r = client.post("/")
        assert r.status_code == 405

    def test_put_method_not_allowed(self):
        r = client.put("/")
        assert r.status_code == 405

    def test_delete_method_not_allowed(self):
        r = client.delete("/")
        assert r.status_code == 405


# ===========================================================================
# GET /health
# ===========================================================================

class TestHealth:
    """Tests for GET /health (liveness probe)."""

    def test_status_200(self):
        r = client.get("/health")
        assert r.status_code == 200

    def test_response_is_json(self):
        r = client.get("/health")
        assert r.headers.get("content-type", "").startswith("application/json")

    def test_exact_body(self):
        r = client.get("/health")
        assert r.json() == {"status": "ok"}

    def test_status_key_present(self):
        r = client.get("/health")
        assert "status" in r.json()

    def test_status_value_is_ok(self):
        r = client.get("/health")
        assert r.json()["status"] == "ok"

    def test_no_extra_keys(self):
        r = client.get("/health")
        assert set(r.json().keys()) == {"status"}

    def test_security_headers(self):
        r = client.get("/health")
        assert_security_headers(r)

    def test_cache_control_no_store(self):
        r = client.get("/health")
        assert "no-store" in r.headers.get("cache-control", "").lower()

    def test_idempotent(self):
        responses = [client.get("/health") for _ in range(3)]
        for r in responses:
            assert r.status_code == 200
            assert r.json() == {"status": "ok"}

    def test_response_time(self):
        r = client.get("/health")
        assert_fast_response(r)

    def test_post_method_not_allowed(self):
        r = client.post("/health")
        assert r.status_code == 405

    def test_put_method_not_allowed(self):
        r = client.put("/health")
        assert r.status_code == 405

    def test_delete_method_not_allowed(self):
        r = client.delete("/health")
        assert r.status_code == 405

    def test_with_query_params_ignored(self):
        """Extra query params should not break the endpoint."""
        r = client.get("/health?foo=bar&baz=1")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_with_accept_json_header(self):
        r = client.get("/health", headers={"Accept": "application/json"})
        assert r.status_code == 200

    def test_with_accept_wildcard_header(self):
        r = client.get("/health", headers={"Accept": "*/*"})
        assert r.status_code == 200


# ===========================================================================
# GET /sitemap.xml
# ===========================================================================

class TestSitemapXml:
    """Tests for GET /sitemap.xml."""

    def test_status_200(self):
        r = client.get("/sitemap.xml")
        assert r.status_code == 200

    def test_content_type_is_xml(self):
        r = client.get("/sitemap.xml")
        assert r.headers.get("content-type", "").startswith("application/xml")

    def test_body_is_not_empty(self):
        r = client.get("/sitemap.xml")
        assert len(r.text.strip()) > 0

    def test_xml_declaration_present(self):
        r = client.get("/sitemap.xml")
        assert r.text.strip().startswith("<?xml")

    def test_urlset_tag_present(self):
        r = client.get("/sitemap.xml")
        assert "<urlset" in r.text

    def test_urlset_closing_tag_present(self):
        r = client.get("/sitemap.xml")
        assert "</urlset>" in r.text

    def test_contains_at_least_one_url(self):
        r = client.get("/sitemap.xml")
        assert "<url>" in r.text or "<url " in r.text

    def test_contains_loc_tag(self):
        r = client.get("/sitemap.xml")
        assert "<loc>" in r.text

    def test_sitemap_namespace(self):
        r = client.get("/sitemap.xml")
        assert "sitemaps.org/schemas/sitemap" in r.text

    def test_cache_control_no_store(self):
        r = client.get("/sitemap.xml")
        assert "no-store" in r.headers.get("cache-control", "").lower()

    def test_security_headers(self):
        r = client.get("/sitemap.xml")
        assert_security_headers(r)

    def test_idempotent(self):
        r1 = client.get("/sitemap.xml")
        r2 = client.get("/sitemap.xml")
        assert r1.status_code == r2.status_code
        assert r1.text == r2.text

    def test_response_time(self):
        r = client.get("/sitemap.xml")
        assert_fast_response(r)

    def test_post_method_not_allowed(self):
        r = client.post("/sitemap.xml")
        assert r.status_code == 405

    def test_parseable_as_xml(self):
        """The response must be parseable by Python's xml.etree module."""
        import xml.etree.ElementTree as ET
        r = client.get("/sitemap.xml")
        try:
            ET.fromstring(r.text)
        except ET.ParseError as exc:
            pytest.fail(f"Sitemap XML is not valid XML: {exc}")


# ===========================================================================
# GET /openapi.json
# ===========================================================================

class TestOpenApiJson:
    """Tests for GET /openapi.json (auto-generated by FastAPI)."""

    def test_status_200(self):
        r = client.get("/openapi.json")
        assert r.status_code == 200

    def test_content_type_is_json(self):
        r = client.get("/openapi.json")
        assert r.headers.get("content-type", "").startswith("application/json")

    def test_body_is_valid_json(self):
        r = client.get("/openapi.json")
        try:
            r.json()
        except Exception as exc:
            pytest.fail(f"Response is not valid JSON: {exc}")

    def test_openapi_version_key_present(self):
        r = client.get("/openapi.json")
        body = r.json()
        assert "openapi" in body, f"Missing 'openapi' key. Keys: {list(body.keys())}"

    def test_openapi_version_is_3x(self):
        r = client.get("/openapi.json")
        version = r.json().get("openapi", "")
        assert version.startswith("3."), f"Expected OpenAPI 3.x, got: '{version}'"

    def test_info_object_present(self):
        r = client.get("/openapi.json")
        assert "info" in r.json()

    def test_info_title_present(self):
        r = client.get("/openapi.json")
        assert "title" in r.json()["info"]

    def test_info_title_not_empty(self):
        r = client.get("/openapi.json")
        assert r.json()["info"]["title"].strip() != ""

    def test_info_version_present(self):
        r = client.get("/openapi.json")
        assert "version" in r.json()["info"]

    def test_paths_object_present(self):
        r = client.get("/openapi.json")
        assert "paths" in r.json()

    def test_paths_contains_health(self):
        r = client.get("/openapi.json")
        assert "/health" in r.json()["paths"]

    def test_paths_contains_api_login(self):
        r = client.get("/openapi.json")
        assert "/api/login" in r.json()["paths"]

    def test_paths_contains_api_contact(self):
        r = client.get("/openapi.json")
        assert "/api/contact" in r.json()["paths"]

    def test_components_present(self):
        r = client.get("/openapi.json")
        body = r.json()
        assert "components" in body or "definitions" in body, (
            "Expected 'components' or 'definitions' in OpenAPI spec"
        )

    def test_security_headers(self):
        r = client.get("/openapi.json")
        assert_security_headers(r)

    def test_cache_control_no_store(self):
        r = client.get("/openapi.json")
        assert "no-store" in r.headers.get("cache-control", "").lower()

    def test_idempotent(self):
        r1 = client.get("/openapi.json")
        r2 = client.get("/openapi.json")
        assert r1.status_code == r2.status_code
        assert r1.json() == r2.json()

    def test_response_time(self):
        r = client.get("/openapi.json")
        assert_fast_response(r)

    def test_post_method_not_allowed(self):
        r = client.post("/openapi.json")
        assert r.status_code == 405


# ===========================================================================
# GET /docs  (Swagger UI)
# ===========================================================================

class TestSwaggerDocs:
    """Tests for GET /docs (Swagger UI served by FastAPI)."""

    def test_status_200(self):
        r = client.get("/docs")
        assert r.status_code == 200

    def test_content_type_is_html(self):
        r = client.get("/docs")
        assert "text/html" in r.headers.get("content-type", "")

    def test_body_contains_swagger(self):
        r = client.get("/docs")
        assert "swagger" in r.text.lower()

    def test_body_contains_openapi_reference(self):
        r = client.get("/docs")
        assert "openapi" in r.text.lower()

    def test_body_not_empty(self):
        r = client.get("/docs")
        assert len(r.text.strip()) > 0

    def test_idempotent(self):
        r1 = client.get("/docs")
        r2 = client.get("/docs")
        assert r1.status_code == r2.status_code

    def test_response_time(self):
        r = client.get("/docs")
        assert_fast_response(r)


# ===========================================================================
# GET /redoc  (ReDoc UI)
# ===========================================================================

class TestRedocDocs:
    """Tests for GET /redoc (ReDoc UI served by FastAPI)."""

    def test_status_200(self):
        r = client.get("/redoc")
        assert r.status_code == 200

    def test_content_type_is_html(self):
        r = client.get("/redoc")
        assert "text/html" in r.headers.get("content-type", "")

    def test_body_contains_redoc(self):
        r = client.get("/redoc")
        assert "redoc" in r.text.lower()

    def test_body_not_empty(self):
        r = client.get("/redoc")
        assert len(r.text.strip()) > 0

    def test_idempotent(self):
        r1 = client.get("/redoc")
        r2 = client.get("/redoc")
        assert r1.status_code == r2.status_code

    def test_response_time(self):
        r = client.get("/redoc")
        assert_fast_response(r)


# ===========================================================================
# 404 — Unknown routes
# ===========================================================================

class TestNotFound:
    """Verify that unknown GET routes return 404."""

    @pytest.mark.parametrize("path", [
        "/unknown",
        "/api",
        "/api/unknown",
        "/healthz",
        "/status",
        "/ping",
        "/v1/health",
        "/health/",
        "/HEALTH",
        "/.env",
        "/admin",
        "/api/users",
    ])
    def test_unknown_route_returns_404(self, path):
        r = client.get(path)
        assert r.status_code == 404, (
            f"Expected 404 for GET {path}, got {r.status_code}"
        )

    def test_404_response_is_json(self):
        r = client.get("/this-does-not-exist")
        assert r.headers.get("content-type", "").startswith("application/json")

    def test_404_body_has_detail_key(self):
        r = client.get("/this-does-not-exist")
        body = r.json()
        assert "detail" in body, f"Expected 'detail' key in 404 body, got: {body}"
