import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:3001"


@events.test_start.add_listener
def seed(environment, **kwargs):
    requests.post(f"{HOST}/seed")


class RestJavaScriptUser(HttpUser):
    host = HOST
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def get_musics(self):
        self.client.get("/musics")

    @task
    def get_playlists(self):
        self.client.get("/playlists")
