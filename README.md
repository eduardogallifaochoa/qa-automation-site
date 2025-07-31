# 🧪 QA Practice Site (Frontend + Backend + Automation)

[![CI](https://github.com/eduardogallifaochoa/qa-automation-site/actions/workflows/test.yml/badge.svg)](https://github.com/eduardogallifaochoa/qa-automation-site/actions/runs/16640021950/job/47088502592)
![Pytest](https://img.shields.io/badge/Pytest-passing-brightgreen)
![Playwright](https://img.shields.io/badge/Playwright-tested-blue)
![Python](https://img.shields.io/badge/python-3.13.5-blue)
[![codecov](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site)


A full QA-friendly project including:

- Static **Frontend** (HTML/CSS/JS)
- FastAPI **Backend** with validation
- **Playwright + Pytest** test suite
- **Docker Compose** for orchestration

Perfect for practicing UI, API, and E2E automation.

## 🚀 Why This Project Matters (Real-World QA Showcase)

This project isn't just a simple demo — it's a **miniature version of what a real QA Engineer would work with** in a professional environment. It simulates a full QA workflow found in companies like **AT&T, IBM, or Mercado Libre**, where **automation, API testing, and CI/CD integration** are must-have skills.

### 🔧 What this project demonstrates:

✅ **Real-world automation testing**:  
Covers login and contact flows with realistic test cases, including **edge cases, security checks, and UI validations**.

✅ **CI/CD Integration**:  
Automatically runs tests on every push to `main` using **GitHub Actions** and uploads a full **HTML test report**, just like in enterprise pipelines.

✅ **Frontend + Backend architecture**:  
Uses **Docker Compose** to simulate a real-life scenario: static frontend served with Nginx + backend API using **FastAPI** — exactly how many modern platforms are built.

✅ **Scalable test structure**:  
Separates tests cleanly with Playwright fixtures, reusable config, and parametric data — making it easy to scale up for future projects or add new features.

✅ **End-to-end coverage**:  
From UI interaction to backend validation, every flow is tested **as a user would experience it**.

---

### 🌍 Example Use in Enterprise QA

Let’s say you’re working for **AT&T** on their customer portal:

- You’d test the **login** form with valid/invalid credentials, same as here.
- The **contact form** would be a support request or service report — tested with long messages, empty fields, etc.
- These tests would be integrated into the CI/CD pipeline — **failures would block deployment**.
- Reports like `report.html` would be attached to **QA dashboards or Jira tickets**, exactly like you're doing here.

---

### 💡 Final Notes

You can plug this same test structure into bigger systems:
- Swap the frontend with React, Angular, or Vue.
- Point the backend to a real API (REST/GraphQL).
- Add **load testing**, **API mocking**, or even **visual regression** with tools like Percy or Playwright snapshots.

## 🖼️ Frontend

Three simple HTML pages:
- `index.html` — Landing page
- `login.html` — Auth form → POST `/api/login`
- `contact.html` — Contact form → POST `/api/contact`

Forms use `fetch()` to send JSON to the backend.

📍 Served via Nginx at: [http://localhost:8080](http://localhost:8080)

## ⚙️ Backend (FastAPI)

Endpoints:
- `POST /api/login` — Hardcoded user check
- `POST /api/contact` — Validated message input

📍 Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

✅ CORS enabled  
✅ Pydantic validation  
✅ Runs via Docker or manually with:
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

---

## 🐳 Docker Compose

Orchestration for frontend + backend.

```bash
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend:/usr/share/nginx/html
    ports:
      - "8080:80"
```
▶ Run both with:
```docker-compose up --build```

## 🧪 Tests (Playwright + Pytest)

Covers:
- Login form inputs (positive & negative)
- Contact form validation (including security & edge cases)

🛠️ Setup:
```bash
pip install -r requirements.txt
playwright install
```

▶ Run tests (headless):
```bash
pytest tests/
```

▶ Or see browser in action:
```bash
pytest tests/ --headed --browser=chromium
```

📍 Targets frontend at `http://localhost:8080`  
Backend must be running.

📄 Generates `report.html` automatically.

## 🗂️ Structure
```
qa-practice-site/
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions workflow (CI/CD)
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Static HTML/CSS/JS site
├── tests/
│   ├── test_contact.py
│   ├── test_login.py
│   └── conftest.py
├── docker-compose.yml
├── playwright.config.json
├── pytest.ini
├── README.md
└── report.html
```

## 📬 Contact

If you're interested in collaborating, have feedback, or just want to geek out about QA automation, feel free to reach out:

- 📧 Email: eduardogallifao@gmail.com  
- 🧑‍💻 GitHub: [eduardogallifaochoa](https://github.com/eduardogallifaochoa)  
- 💼 LinkedIn: [Eduardo Gallifa Ochoa](https://www.linkedin.com/in/eduardogallifaochoa/)

Always open to new challenges and QA opportunities!