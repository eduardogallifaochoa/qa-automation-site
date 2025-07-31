import pytest
import logging

# Test data for contact form
contact_data = [
    # (name, email, message, description)
    ("Eddie", "eddie@mail.com", "This is a valid message.", "Valid input"),
    ("Eddie", "eddie[at]mail", "Hi there", "Invalid email format"),
    ("E", "eddie@mail.com", "Hi there", "Too short name"),
    ("Eddie", "eddie@mail.com", "Hey", "Too short message"),
    ("", "", "", "All fields empty"),
    ("Eddie", "eddie@mail.com", "A" * 501, "Message too long"),
    ("Eddie", "EDDIE@GMAIL.COM", "Hello there.", "Email uppercase"),
    ("Eddie", "eddie@mail.com", "<b>Hello</b>", "Message with HTML tags"),
    ("Édgar Núñez", "edgar@mail.com", "Hola desde México.", "Name with accents"),

    # New security & edge cases
    ("<script>alert(1)</script>", "xss@mail.com", "Trying XSS", "XSS in name"),
    ("Eddie", "eddie@mail.com", "' OR '1'='1", "SQL injection in message"),
    ("<img src=x onerror=alert(1)>", "hack@hack.com", "Image XSS", "XSS in email"),
    ("a" * 255, "test@test.com", "Normal message", "Name max length"),
    ("Eddie", "test@" + "a"*240 + ".com", "Hi", "Email long domain"),
    ("Eddie", "eddie@mail.com", "\n\t\r", "Message with escape characters"),
    ("   Eddie   ", "   eddie@mail.com   ", "   trimmed?   ", "Inputs with extra spaces"),
    ("Eddie", "éd.dié@mail.com", "Hola", "Email with special unicode"),
    ("Eddie", "contact+qa@mail.com", "Testing plus alias", "Email with +alias"),
]

@pytest.mark.parametrize(
    "name,email,message",
    [ (n, e, m) for n, e, m, _ in contact_data ],
    ids=[desc for _, _, _, desc in contact_data]
)
def test_contact_form_cases(page, name, email, message):
    page.goto("http://localhost:8080/contact.html")
    page.fill("#name", name)
    page.fill("#email", email)
    page.fill("#message", message)
    logging.info(f"Tested with name='{name}', email='{email}', message='{message}'")
    page.click("button[type='submit']")
    page.wait_for_timeout(1000)
