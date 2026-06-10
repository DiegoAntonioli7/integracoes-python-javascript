from pathlib import Path

import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:3001"
RESPONSE_FILE = Path(__file__).parent / "rest_javascript_response.txt"


@events.test_start.add_listener
def seed_and_save_sample(environment, **kwargs):
    requests.post(f"{HOST}/seed")
    response = requests.get(f"{HOST}/musics")
    RESPONSE_FILE.write_text(response.text, encoding="utf-8")


class RestJavaScriptUser(HttpUser):
    host = HOST
    wait_time = between(0.05, 0.2)

    @task(3)
    def get_musics(self):
        self.client.get("/musics", name="GET /musics")

    @task(2)
    def get_playlists(self):
        self.client.get("/playlists", name="GET /playlists")

    @task(1)
    def get_users(self):
        self.client.get("/users", name="GET /users")
