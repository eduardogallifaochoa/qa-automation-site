from locust import HttpUser, task, between

LOGIN_PAYLOAD = {"username": "admin", "password": "1234"}
CONTACT_PAYLOAD = {"name": "Eddie", "email": "a@b.com", "message": "Hello from QA site!"}
HEADERS = {"Content-Type": "application/json"}

class QaUser(HttpUser):
    wait_time = between(0.2, 1.0)  # pequeño pacing

    def on_start(self):
        # Login una vez por usuario; HttpUser mantiene cookies/sesión.
        with self.client.post("/api/login", json=LOGIN_PAYLOAD, headers=HEADERS, catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Login failed: {res.status_code} {res.text}")

    @task(3)
    def contact(self):
        with self.client.post("/api/contact", json=CONTACT_PAYLOAD, headers=HEADERS, catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Contact failed: {res.status_code} {res.text}")

    @task(1)
    def occasional_relogin(self):
        # De vez en cuando renueva sesión para simular expiraciones.
        with self.client.post("/api/login", json=LOGIN_PAYLOAD, headers=HEADERS, catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Re-login failed: {res.status_code} {res.text}")
