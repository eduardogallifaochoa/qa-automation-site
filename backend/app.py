from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Enable CORS to allow frontend (on port 8080) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:8080"]
    allow_methods=["*"],
    allow_headers=["*"]
)

# Simulated user database
users_db = {
    "admin": "1234",
    "testuser": "password123",
}

# Request body model for login endpoint
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=4, max_length=30)

# Request body model for contact endpoint
class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=500)

# Handle POST requests to /api/login
@app.post("/api/login")
def login(data: LoginRequest):
    if data.username in users_db and users_db[data.username] == data.password:
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Handle POST requests to /api/contact
@app.post("/api/contact")
def contact(data: ContactRequest):
    # In a real app, you might store this in a database or send an email
    print(f"New contact from {data.name} <{data.email}>: {data.message}")
    return {"message": "Message received"}
