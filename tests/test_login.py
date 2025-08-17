# tests/test_login.py

import pytest
import logging

# Test data for login form
login_data = [
    # (username, password, description)
    ("admin", "1234", "Valid admin credentials"),
    ("testuser", "password123", "Valid testuser credentials"),
    ("admin", "wrongpass", "Wrong password"),
    ("notfound", "1234", "Non-existent user"),
    ("", "", "Empty fields"),
    ("ab", "1234", "Username too short"),
    ("admin", "123", "Password too short"),
    ("a" * 25, "1234", "Username too long"),
    ("admin", "p" * 35, "Password too long"),
    ("admin<script>", "1234@#$%", "XSS & special chars"),
    (" admin ", " 1234 ", "Leading/trailing spaces"),
    ("ADMIN", "1234", "Uppercase username"),
    ("admin", "' OR '1'='1", "SQL injection password"),
    ("user<script>alert()</script>", "pass", "Script in username"),
    ("<img src=x onerror=alert(1)>", "password", "XSS vector in username"),
    ("user", "pass\n", "Password with newline"),
    ("user", "pass\t", "Password with tab"),
]

@pytest.mark.parametrize(
    "username,password",
    [ (u, p) for u, p, _ in login_data ],
    ids=[desc for _, _, desc in login_data]
)
def test_login_cases(page, username, password):
    page.goto("http://localhost:8080/login.html")
    page.fill("#username", username)
    page.fill("#password", password)
    logging.info(f"Tested with username='{username}' and password='{password}'")
    page.click("button[type='submit']")
    page.wait_for_timeout(1000)
