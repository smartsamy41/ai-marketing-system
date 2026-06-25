import os
import requests
from requests.auth import HTTPBasicAuth


class TarifcheckSalesEngine:

    def __init__(self):

        self.username = os.getenv("TARIFCHECK_USERNAME")
        self.password = os.getenv("TARIFCHECK_PASSWORD")
        self.url = os.getenv(
            "TARIFCHECK_API_URL",
            "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"
        )

    def fetch_leads(self):

        if not self.username or not self.password:
            return {
                "status": "ERROR",
                "message": "Missing ENV credentials"
            }

        try:
            response = requests.get(
                self.url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=20
            )

            return {
                "status": "SUCCESS",
                "code": response.status_code,
                "leads": response.json().get("data", [])
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }
