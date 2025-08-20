# app/main.py
from typing import Literal

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="QA Automation API", version="0.1.0")


# ---------- Models ----------
class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class ErrorMessage(BaseModel):
    detail: str = "Invalid credentials"


class ContactIn(BaseModel):
    # Defaults help fuzzing & docs examples
    name: str = "John Tester"
    email: EmailStr = "john@example.com"
    message: str = "Hello!"


class ContactOut(BaseModel):
    ok: bool = True


# ---------- Security headers middleware ----------
@app.middleware("http")
async def security_headers(request: Request, call_next):
    """
    Add a minimal set of security headers.
    - X-Content-Type-Options: prevent MIME sniffing
    - COOP/COEP/CORP: useful for Spectre isolation; keep strict in dev
    - Cache-Control: no-store to silence ZAP "storable content" in dev
      (tweak for prod as needed, e.g., static assets can be cached).
    """
    resp: Response = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    resp.headers.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
    resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
    resp.headers.setdefault("Cache-Control", "no-store")
    return resp


# ---------- API endpoints ----------
@app.post(
    "/api/login",
    response_model=LoginOut,
    tags=["API"],
    summary="Login",
    # Document 401 so Schemathesis doesn't fail on unauthorized cases
    responses={
        401: {
            "description": "Unauthorized - Invalid credentials",
            "model": ErrorMessage,
        }
    },
)
async def login(payload: LoginIn) -> LoginOut:
    """
    Dummy login: returns a static bearer token for testing purposes.
    In real implementations you may return 401 when credentials are invalid.
    """
    return LoginOut(access_token="fake-token-for-tests")


@app.post("/api/contact", response_model=ContactOut, tags=["API"], summary="Contact")
async def contact(payload: ContactIn) -> ContactOut:
    """
    Accept a contact message and return a simple OK response.
    """
    # In real life, enqueue/send email, persist, etc.
    return ContactOut(ok=True)


# ---------- Utility endpoints (out of schema or simple) ----------
@app.get("/health", tags=["Utility"], summary="Health check")
async def health() -> dict:
    """Simple liveness probe for monitors & CI."""
    return {"status": "ok"}


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap() -> Response:
    """
    Minimal sitemap to avoid 404s in scanners.
    Served with no-store to keep ZAP happy in dev.
    """
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>http://localhost:8000/</loc></url>
  <url><loc>http://localhost:8000/docs</loc></url>
</urlset>"""
    return Response(content=xml, media_type="application/xml", headers={"Cache-Control": "no-store"})


# Optional root for friendliness (not required)
@app.get("/", include_in_schema=False)
async def root() -> JSONResponse:
    return JSONResponse({"message": "QA Automation API is up"})
