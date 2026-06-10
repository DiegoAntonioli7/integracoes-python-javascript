from pathlib import Path

import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:8001"
NS = "http://streaming.api.com/v1"
HEADERS = {"Content-Type": "text/xml", "SOAPAction": ""}
RESPONSE_FILE = Path(__file__).parent / "soap_python_response.txt"


def soap_body(operation):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="{NS}">
  <soapenv:Body><tns:{operation}/></soapenv:Body>
</soapenv:Envelope>"""


@events.test_start.add_listener
def seed_and_save_sample(environment, **kwargs):
    requests.post(HOST, data=soap_body("Seed"), headers={**HEADERS, "SOAPAction": f'"{NS}#Seed"'})
    response = requests.post(
        HOST,
        data=soap_body("GetMusics"),
        headers={**HEADERS, "SOAPAction": f'"{NS}#GetMusics"'},
    )
    RESPONSE_FILE.write_text(response.text, encoding="utf-8")


class SoapPythonUser(HttpUser):
    host = HOST
    wait_time = between(0.05, 0.2)

    @task(3)
    def get_musics(self):
        self.client.post(
            "/",
            data=soap_body("GetMusics"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetMusics"'},
            name="GetMusics",
        )

    @task(2)
    def get_playlists(self):
        self.client.post(
            "/",
            data=soap_body("GetPlaylists"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetPlaylists"'},
            name="GetPlaylists",
        )

    @task(1)
    def get_users(self):
        self.client.post(
            "/",
            data=soap_body("GetUsers"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetUsers"'},
            name="GetUsers",
        )
