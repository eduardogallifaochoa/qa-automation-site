# tests/visual/test_login_visual.py
from playwright.sync_api import Page, expect
import os
import re

# Force IPv4 to avoid IPv6 (::1) issues
FRONTEND = os.getenv("FRONTEND_URL", "http://127.0.0.1:8080")

def test_login_visual(page: Page):
    # Navigate to the login page served by the frontend
    url = f"{FRONTEND}/login.html"
    resp = page.goto(url)
    # Fail early with clear message if not 2xx
    assert resp is not None and resp.ok, f"GET {url} failed with status {getattr(resp, 'status', None)}"

    # Title should contain 'Login' (case-insensitive)
    expect(page).to_have_title(re.compile(r"Login", re.I))

    # Ensure the form is visible before taking the snapshot
    expect(page.locator("#loginForm")).to_be_visible()

    # Visual snapshot (baseline required on first run)
    expect(page).to_have_screenshot("login.png", full_page=True)
