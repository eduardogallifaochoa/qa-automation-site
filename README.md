# 🧪 QA Automation Site (UI + API + CI/CD)

[![Tests](https://github.com/eduardogallifaochoa/qa-automation-site/actions/workflows/test.yml/badge.svg)](https://github.com/eduardogallifaochoa/qa-automation-site/actions/workflows/test.yml)
![Playwright](https://img.shields.io/badge/Playwright-tested-blue)
![Pytest](https://img.shields.io/badge/Pytest-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
[![codecov](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site/branch/main/graph/badge.svg?token=REPLACE_WITH_CODECOV_TOKEN)](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site)

A production-style QA automation practice repo:
- Static frontend (Login + Contact)
- FastAPI backend with validation + OpenAPI
- Tests: Playwright (UI) + Pytest (API) + Schemathesis (OpenAPI fuzz)
- Docker Compose + GitHub Actions CI

## 🔗 Local URLs
- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

## 🚀 Run the app (Docker)
```bash
docker compose up -d --build
```

Stop:
```bash
docker compose down
```

## ✅ Run tests (local)
Install deps:
```bash
python -m venv .venv
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
playwright install
```

UI tests (Playwright):
```bash
pytest tests/visual --html=report.html --self-contained-html
```

API tests (Pytest):
```bash
pytest -q tests/api
```

OpenAPI fuzz (Schemathesis):
```bash
schemathesis run http://127.0.0.1:8000/openapi.json \
  --url http://127.0.0.1:8000 \
  --checks all \
  --max-examples 10
```

## 🤖 CI
- test.yml: Docker Compose + UI/API tests + HTML report artifact + coverage to Codecov
- fuzz.yml: starts FastAPI + runs Schemathesis fuzzing

> Codecov: set CODECOV_TOKEN in GitHub repo secrets.  
> Replace REPLACE_WITH_CODECOV_TOKEN in the badge URL if you want the badge to reflect your repo token.

## 🗂️ Structure (high level)
```text
frontend/   # Static HTML/CSS/JS
app/        # Minimal FastAPI app (uvicorn app.main:app)
backend/    # Compose backend service
tests/
  api/      # API tests (TestClient)
  visual/   # UI tests (Playwright)
  fuzz/     # Schemathesis wrapper/tests
.github/    # CI workflows
```

## 💬 Contact
- Email: eduardogallifao@gmail.com
- GitHub: https://github.com/eduardogallifaochoa
- LinkedIn: https://www.linkedin.com/in/eduardogallifaochoa/
