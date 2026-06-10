import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:3002"
HEADERS = {"Content-Type": "text/xml"}


def soap_body(operation):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body><{operation}/></soapenv:Body>
</soapenv:Envelope>"""


@events.test_start.add_listener
def seed(environment, **kwargs):
    requests.post(HOST, data=soap_body("Seed"), headers={**HEADERS, "SOAPAction": "Seed"})


class SoapJavaScriptUser(HttpUser):
    host = HOST
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        self.client.post(
            "/",
            data=soap_body("GetUsers"),
            headers={**HEADERS, "SOAPAction": "GetUsers"},
            name="GetUsers",
        )

    @task
    def get_musics(self):
        self.client.post(
            "/",
            data=soap_body("GetMusics"),
            headers={**HEADERS, "SOAPAction": "GetMusics"},
            name="GetMusics",
        )

    @task
    def get_playlists(self):
        self.client.post(
            "/",
            data=soap_body("GetPlaylists"),
            headers={**HEADERS, "SOAPAction": "GetPlaylists"},
            name="GetPlaylists",
        )
