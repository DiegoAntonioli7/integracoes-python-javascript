from pathlib import Path

import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:8000"
USERS_QUERY = "/users"
MUSICS_QUERY = "/musics"
PLAYLISTS_QUERY = "/playlists"
RESPONSE_FILE = Path(__file__).parent / "rest_python_response.txt"


@events.test_start.add_listener
def seed_and_save_sample(environment, **kwargs):
    requests.post(f"{HOST}/seed")
    response = requests.get(f"{HOST}{MUSICS_QUERY}")
    RESPONSE_FILE.write_text(response.text, encoding="utf-8")


class RestPythonUser(HttpUser):
    host = HOST
    wait_time = between(0.05, 0.2)

    @task(3)
    def get_musics(self):
        self.client.get(MUSICS_QUERY, name="GET /musics")

    @task(2)
    def get_playlists(self):
        self.client.get(PLAYLISTS_QUERY, name="GET /playlists")

    @task(1)
    def get_users(self):
        self.client.get(USERS_QUERY, name="GET /users")
