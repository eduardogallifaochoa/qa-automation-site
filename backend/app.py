# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="QA Automation API (compose backend)", version="0.1.0")

# Enable CORS to allow frontend (on port 8080) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost:8080"] si quieres
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated user database
users_db = {
    "admin": "1234",
    "testuser": "password123",
}

# ---------- Models ----------
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=4, max_length=30)

class LoginResponse(BaseModel):
    message: str = "Login successful"

class ErrorMessage(BaseModel):
    detail: str = "Invalid credentials"

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=500)

class ContactResponse(BaseModel):
    message: str = "Message received"

# ---------- Endpoints ----------
@app.post(
    "/api/login",
    response_model=LoginResponse,
    tags=["API"],
    summary="Login",
    # We document the 401 Unauthorized response
    responses={
        401: {
            "description": "Unauthorized - Invalid credentials",
            "model": ErrorMessage,
        }
    },
)
def login(data: LoginRequest):
    if data.username in users_db and users_db[data.username] == data.password:
        return LoginResponse()
    # This 401 response is documented for Schemathesis
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post(
    "/api/contact",
    response_model=ContactResponse,
    tags=["API"],
    summary="Contact",
)
def contact(data: ContactRequest):
    # En una app real: persistir/enviar email/cola, etc.
    print(f"New contact from {data.name} <{data.email}>: {data.message}")
    return ContactResponse()
