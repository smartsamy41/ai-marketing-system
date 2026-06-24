import requests
from requests.auth import HTTPBasicAuth


# =========================
# TARIFCHECK SALES API ENGINE
# =========================
class TarifcheckSalesEngine:

    def __init__(self, password):

        self.username = "partner_165274"
        self.password = password
        self.url = "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"

    # =========================
    # FETCH LEADS
    # =========================
    def fetch_leads(self):

        try:
            response = requests.get(
                self.url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=20
            )

            data = response.json()

            return {
                "status": "SUCCESS",
                "leads": data.get("data", [])
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e)
            }
