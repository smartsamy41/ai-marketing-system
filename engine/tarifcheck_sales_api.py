import requests
from google.cloud import secretmanager


class TarifcheckSalesAPI:


    def __init__(self):

        self.client = secretmanager.SecretManagerServiceClient()

        self.project = "smartcontent2050"

        self.username = self.get_secret(
            "TARIFCHECK_API_USERNAME"
        )

        self.password = self.get_secret(
            "TARIFCHECK_API_PASSWORD"
        )

        self.url = self.get_secret(
            "TARIFCHECK_API_URL"
        )


    def get_secret(self, name):

        path = (
            f"projects/{self.project}"
            f"/secrets/{name}/versions/latest"
        )

        response = self.client.access_secret_version(
            request={
                "name": path
            }
        )

        return response.payload.data.decode(
            "UTF-8"
        )


    def get_leads(self):

        response = requests.get(
            self.url,
            auth=(
                self.username,
                self.password
            ),
            timeout=30
        )

        response.raise_for_status()

        return response.json()
