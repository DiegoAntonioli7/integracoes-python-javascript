import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:8002"
ENDPOINT = "/graphql"
HEADERS = {"Content-Type": "application/json"}


@events.test_start.add_listener
def seed(environment, **kwargs):
    requests.post(
        f"{HOST}{ENDPOINT}",
        json={"query": "mutation { seed }"},
        headers=HEADERS,
    )


class GraphQLPythonUser(HttpUser):
    host = HOST
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        self.client.post(
            ENDPOINT,
            json={"query": "{ users { id name email } }"},
            headers=HEADERS,
            name="query:users",
        )

    @task
    def get_musics(self):
        self.client.post(
            ENDPOINT,
            json={"query": "{ musics { id title artist album duration } }"},
            headers=HEADERS,
            name="query:musics",
        )

    @task
    def get_playlists(self):
        self.client.post(
            ENDPOINT,
            json={"query": "{ playlists { id user_id name description } }"},
            headers=HEADERS,
            name="query:playlists",
        )
