# app/main.py
from fastapi import FastAPI, Request, APIRouter
from pydantic import BaseModel

app = FastAPI(
    title="QA Automation API",
    version="0.1.0",
    # Force OpenAPI 3.0 for better tooling compatibility (Schemathesis 4.x)
    openapi_version="3.0.3",
)

# -------------------- Security headers middleware --------------------
@app.middleware("http")
async def security_headers(request: Request, call_next):
    resp = await call_next(request)
    # Do not override if already set upstream (use setdefault).
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    resp.headers.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
    resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
    # Avoid caching sensitive responses during testing.
    resp.headers.setdefault("Cache-Control", "no-store")
    return resp

# -------------------- Demo API (used by perf tests) --------------------
router = APIRouter(prefix="/api", tags=["API"])

class LoginIn(BaseModel):
    username: str
    password: str

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginOut)
async def login(payload: LoginIn):
    # Minimal stub; replace with real auth if needed.
    return LoginOut(access_token=f"fake-token-for-{payload.username}")

class ContactIn(BaseModel):
    name: str = "John Tester"
    email: str = "john@example.com"
    message: str = "Hello!"

@router.post("/contact")
async def contact(payload: ContactIn):
    # Minimal stub; replace with real processing if needed.
    return {"status": "ok", "received": payload.model_dump()}

app.include_router(router)
