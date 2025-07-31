import pytest
from playwright.sync_api import sync_playwright

# Fixture to launch Playwright browser (headed or headless)
@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Change to True if you don't want to see browser
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
