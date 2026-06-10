from pathlib import Path

import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:8002"
ENDPOINT = "/graphql"
HEADERS = {"Content-Type": "application/json"}
RESPONSE_FILE = Path(__file__).parent / "graphql_python_response.txt"

USERS_QUERY = """
{
  users {
    id name email country city bio phone avatar_url
  }
}
"""

MUSICS_QUERY = """
{
  musics {
    id title artist album duration genre label composer lyrics_snippet cover_url
  }
}
"""

PLAYLISTS_QUERY = """
{
  playlists {
    id user_id name description genre_tags mood cover_url notes
  }
}
"""


@events.test_start.add_listener
def seed_and_save_sample(environment, **kwargs):
    requests.post(
        f"{HOST}{ENDPOINT}",
        json={"query": "mutation { seed }"},
        headers=HEADERS,
    )
    response = requests.post(
        f"{HOST}{ENDPOINT}",
        json={"query": MUSICS_QUERY},
        headers=HEADERS,
    )
    RESPONSE_FILE.write_text(response.text, encoding="utf-8")


class GraphQLPythonUser(HttpUser):
    host = HOST
    wait_time = between(0.05, 0.2)

    @task(3)
    def get_musics(self):
        self.client.post(
            ENDPOINT,
            json={"query": MUSICS_QUERY},
            headers=HEADERS,
            name="query:musics",
        )

    @task(2)
    def get_playlists(self):
        self.client.post(
            ENDPOINT,
            json={"query": PLAYLISTS_QUERY},
            headers=HEADERS,
            name="query:playlists",
        )

    @task(1)
    def get_users(self):
        self.client.post(
            ENDPOINT,
            json={"query": USERS_QUERY},
            headers=HEADERS,
            name="query:users",
        )
