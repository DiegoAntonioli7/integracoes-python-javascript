from pathlib import Path

import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:3002"
HEADERS = {"Content-Type": "text/xml"}
RESPONSE_FILE = Path(__file__).parent / "soap_javascript_response.txt"


def soap_body(operation):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body><{operation}/></soapenv:Body>
</soapenv:Envelope>"""


@events.test_start.add_listener
def seed_and_save_sample(environment, **kwargs):
    requests.post(HOST, data=soap_body("Seed"), headers={**HEADERS, "SOAPAction": "Seed"})
    response = requests.post(
        HOST,
        data=soap_body("GetMusics"),
        headers={**HEADERS, "SOAPAction": "GetMusics"},
    )
    RESPONSE_FILE.write_text(response.text, encoding="utf-8")


class SoapJavaScriptUser(HttpUser):
    host = HOST
    wait_time = between(0.05, 0.2)

    @task(3)
    def get_musics(self):
        self.client.post(
            "/",
            data=soap_body("GetMusics"),
            headers={**HEADERS, "SOAPAction": "GetMusics"},
            name="GetMusics",
        )

    @task(2)
    def get_playlists(self):
        self.client.post(
            "/",
            data=soap_body("GetPlaylists"),
            headers={**HEADERS, "SOAPAction": "GetPlaylists"},
            name="GetPlaylists",
        )

    @task(1)
    def get_users(self):
        self.client.post(
            "/",
            data=soap_body("GetUsers"),
            headers={**HEADERS, "SOAPAction": "GetUsers"},
            name="GetUsers",
        )
