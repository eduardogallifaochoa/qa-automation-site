# 🧪 QA Automation Site — Frontend + FastAPI + CI/CD

[![Tests](https://github.com/eduardogallifaochoa/qa-automation-site/actions/workflows/test.yml/badge.svg)](https://github.com/eduardogallifaochoa/qa-automation-site/actions/workflows/test.yml)
![Playwright](https://img.shields.io/badge/Playwright-tested-blue)
![Pytest](https://img.shields.io/badge/Pytest-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
[![codecov](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/eduardogallifaochoa/qa-automation-site)

A realistic QA practice project that mirrors production setups:

- Static **frontend** (HTML/CSS/JS) with Login & Contact flows  
- **FastAPI** backend with validation and OpenAPI (3.1)  
- Test suite: **Playwright** (UI), **Pytest** (API), **Schemathesis** (OpenAPI fuzz)  
- **Docker Compose** orchestration + **GitHub Actions** CI

---

## ⚙️ Architecture & URLs

- **Frontend**: static pages served by Nginx  
  - `http://localhost:8080/` (index)  
  - `http://localhost:8080/login.html`  
  - `http://localhost:8080/contact.html`
- **Backend**: FastAPI app  
  - `http://localhost:8000/` (health)  
  - `http://localhost:8000/docs` (Swagger UI)  
  - `http://localhost:8000/openapi.json` (OpenAPI)  
  - `POST /api/login` & `POST /api/contact`

---

## 🚀 Quick Start (Docker)

```bash
# Start everything
docker compose up -d --build

# Stop
docker compose down
```
Open:

Frontend → ```http://localhost:8080```

Backend docs → ```http://localhost:8000/docs```

## 🧑‍💻 Quick Start (Manual Dev)

Backend:
```bash
# In repo root (or cd backend if you prefer)
python -m venv .venv
# Windows PowerShell
. .\.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Frontend (serve static files locally):
```bash
cd frontend
# Simple Python HTTP server
python -m http.server 8080
# Now open http://localhost:8080
```
## ✅ Running Tests Locally
### 1) UI (Playwright)
```bash
pip install -r requirements.txt
playwright install
pytest tests/ --html=report.html --self-contained-html
```
Flags you make like:
- ```--headed --browser=chromium``` to see the browser
- ```-k "login or contact"``` to filter tests

### 2) API (Pytest)
```bash
pytest -q tests/api/test_endpoints.py
```
### 3) OpenAPI Fuzz (Schemathesis)

CLI:
```bash
schemathesis run http://127.0.0.1:8000/openapi.json \
  --url http://127.0.0.1:8000 \
  --checks all \
  --max-examples 10
```
Pytest wrapper (uses the CLI under the hood):
```bash
# Optional (but handy) env vars
$env:OPENAPI_URL="http://127.0.0.1:8000/openapi.json"   # PowerShell
$env:BASE_URL="http://127.0.0.1:8000"
$env:FUZZ_EXAMPLES="10"
pytest -q tests/fuzz/test_openapi.py
```

---

## 🤖 CI/CD (GitHub Actions)

There are two key workflows:

1) **`test.yml` (UI + API + Compose)**
- Builds/starts the stack with `docker compose`
- Waits for the frontend to be ready
- Installs Python deps & Playwright browsers
- Runs Playwright + Pytest suite
- Uploads `report.html` artifact
- Publishes coverage to Codecov

2) **`fuzz.yml` (Schemathesis)**
- Installs Python deps
- Boots the FastAPI app (Uvicorn) in background
- Runs `schemathesis run ... --url ... --checks all --max-examples 10`
- Runs the Pytest wrapper `tests/fuzz/test_openapi.py`

> **Codecov:** set `CODECOV_TOKEN` in repo secrets if you want upload to succeed.


## 🗂️ Project Structure
```markdown
.
├─ .github/workflows/
│  ├─ test.yml          # UI CI (Playwright) + Docker Compose → uses backend/
│  └─ fuzz.yml          # Fuzz CI (Schemathesis) → uses app/
├─ app/                 # Minimal FastAPI app (uvicorn app.main:app)
├─ backend/             # Original backend used by docker-compose.yml
├─ frontend/            # Static HTML (index/login/contact)
├─ tests/
│  ├─ api/              # API tests with TestClient → import app.main
│  ├─ fuzz/             # Schemathesis CLI wrapper
│  └─ visual/           # Playwright UI tests → target the frontend (8080)
├─ docker-compose.yml   # Starts backend/ + nginx for frontend/
├─ requirements.txt         # General dependencies (app + tests)
├─ requirements-dev.txt     # Dev extras (includes Windows-only stuff like pywin32)
├─ requirements-fuzz.txt    # Optional if you separate fuzz deps
├─ pytest.ini
└─ (local artifacts to ignore: .venv, .ruff_cache, .hypothesis, report.html, zap.out)
```


---

## 🧹 Lint & Security Checks
```bash
# Ruff (lint/format)
ruff check . --fix

# Bandit (security static analysis)
bandit -r app -ll

# pip-audit (dependency vulnerabilities)
pip-audit -r requirements.txt
```

---

## 🪟 Windows Tips
If you see a UnicodeEncodeError when running Schemathesis CLI (especially due to the console codepage), force UTF-8 for the session:
```powershell
# PowerShell
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"
schemathesis run http://127.0.0.1:8000/openapi.json --url http://127.0.0.1:8000 --checks all --max-examples 10
```

---


## 🧰 Troubleshooting

### Schemathesis CLI flag differences (v4.x)
Use ```--url``` instead of ```--base-url```.
Example:
```schemathesis run <openapi> --url http://127.0.0.1:8000 --checks all --max-examples 10```

### “from_uri / loaders / load” import errors
Use the CLI or the newer API surface. The test wrapper calls the CLI to avoid import churn across versions.

### OpenAPI 3.1
Schemathesis v4 handles loading 3.1 but may skip “Examples” phase. Coverage & fuzzing still run.

### Playwright missing browsers
Run ```playwright install``` at least once in your environment.

### Docker Compose not ready yet
CI waits with a curl loop. Locally, ensure http://localhost:8080 and http://localhost:8000/openapi.json respond before launching tests.

---

## 📥 Artifacts & Reports

- **HTML test report:** `report.html` (uploaded by CI; downloadable from the Actions run)
- **Coverage:** uploaded to **Codecov** (requires secret)
- **Schemathesis:** full CLI output in the job logs

## 🧭 Roadmap Ideas

- Visual regression (Playwright snapshots / Percy)
- Load testing (Locust) against `/api/*`
- Contract tests pinned to OpenAPI examples
- Dockerized Playwright service for parallel UI runs

## 🎯 Showcase

This project demonstrates a broad, job-ready QA automation skillset across UI, API, CI/CD, and tooling:

### Full-stack testing in one repo
- **Frontend + Backend + Tests** together: static site (Nginx) + FastAPI service + Playwright/Pytest suites.
- **Docker Compose** orchestrates the stack locally just like a real system.

### API design & correctness
- **FastAPI** app with `pydantic` validation, clean request/response models, and a published **OpenAPI 3.1** spec.
- **Security headers** & **CORS** configured (e.g., `X-Content-Type-Options`, COOP/COEP/CORP).
- Healthcheck & sitemap endpoints for basic ops readiness.

### E2E UI automation (Playwright)
- **Data-driven tests** for login & contact forms (valid/invalid, boundaries, trimming, unicode, long inputs).
- **Security-minded cases** (XSS/SQLi strings, HTML in inputs, whitespace/newlines).
- **Headless/headed** runs with fixtures, stable selectors, and structured logs.

### API testing (Pytest + TestClient)
- **Unit/integration** tests directly against the FastAPI app (no network flakiness).
- Parametrized cases with clear assertions and descriptive IDs.
- **HTML reports** and **coverage** output for quick triage & quality metrics.

### Spec-based fuzzing (Schemathesis)
- CLI-driven **property-based testing** against the OpenAPI spec.
- Handles the **v4 CLI flags** (`--url` instead of `--base-url`) and OpenAPI 3.1 behavior.
- **Pytest wrapper** to exercise the CLI end-to-end and capture regressions.
- Configurable **example budget** (`--max-examples`) for fast/slow builds.

### CI/CD on GitHub Actions
- **Two pipelines**:
  - `test.yml`: builds Docker stack, waits for readiness, runs Playwright+Pytest, uploads `report.html`, sends coverage to **Codecov**.
  - `fuzz.yml`: boots the FastAPI app (uvicorn), runs **Schemathesis** CLI & the Pytest wrapper.
- **Caching** for pip & Playwright browsers, **UTF-8 env** fixes on Linux/Windows runners.
- Artifacts searchable in Actions; **coverage badge** ready.

### Quality & security gates
- **Ruff** for lint/format (fast & strict).
- **Bandit** for static security analysis.
- **pip-audit** for dependency CVEs (CycloneDX support included).

### Cross-platform & DevX polish
- Works on **Windows & Linux**; includes **Unicode** console workarounds for Schemathesis.
- Deterministic seeds in CLI output; actionable **curl repro** lines from failures.
- Clean project layout: `tests/api` (TestClient), `tests/visual` (Playwright), `tests/fuzz` (Schemathesis).

### Scale & future-proofing
- Clear separation of suites enables **parallelization** or selective runs.
- **Locust** & performance testing hooks available for future load tests.
- Easy to extend to visual regression (Playwright snapshots/Percy) or contract tests pinned to OpenAPI examples.

> TL;DR — This repo mirrors a real QA pipeline: **spec-driven API testing, UI automation, security checks, CI/CD, reporting, and Dockerized environments**—all production-style.


## 💬 Contact

- 📧 Email: eduardogallifao@gmail.com  
- 🧑‍💻 GitHub: [eduardogallifaochoa](https://github.com/eduardogallifaochoa)  
- 💼 LinkedIn: [Eduardo Gallifa Ochoa](https://www.linkedin.com/in/eduardogallifaochoa/)

PRs and issues welcome!

