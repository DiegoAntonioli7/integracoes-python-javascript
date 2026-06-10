import requests
from locust import HttpUser, task, between, events

HOST = "http://localhost:8001"
NS = "http://streaming.api.com/v1"
HEADERS = {"Content-Type": "text/xml", "SOAPAction": ""}


def soap_body(operation):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="{NS}">
  <soapenv:Body><tns:{operation}/></soapenv:Body>
</soapenv:Envelope>"""


@events.test_start.add_listener
def seed(environment, **kwargs):
    requests.post(HOST, data=soap_body("Seed"), headers={**HEADERS, "SOAPAction": f'"{NS}#Seed"'})


class SoapPythonUser(HttpUser):
    host = HOST
    wait_time = between(0.1, 0.5)

    @task
    def get_users(self):
        self.client.post(
            "/",
            data=soap_body("GetUsers"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetUsers"'},
            name="GetUsers",
        )

    @task
    def get_musics(self):
        self.client.post(
            "/",
            data=soap_body("GetMusics"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetMusics"'},
            name="GetMusics",
        )

    @task
    def get_playlists(self):
        self.client.post(
            "/",
            data=soap_body("GetPlaylists"),
            headers={**HEADERS, "SOAPAction": f'"{NS}#GetPlaylists"'},
            name="GetPlaylists",
        )
