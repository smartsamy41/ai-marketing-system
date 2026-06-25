import os
import requests
from requests.auth import HTTPBasicAuth


class TarifcheckSalesEngine:

    def __init__(self):

        # =========================
        # ENV CONFIG
        # =========================
        self.username = os.getenv("TARIFCHECK_USERNAME")
        self.password = os.getenv("TARIFCHECK_PASSWORD")

        self.url = os.getenv(
            "TARIFCHECK_API_URL",
            "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"
        )

    # =========================
    # FETCH LEADS (SAFE VERSION)
    # =========================
    def fetch_leads(self):

        # -------------------------
        # CHECK ENV
        # -------------------------
        if not self.username or not self.password:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": "ENV MISSING (USERNAME or PASSWORD)",
                "code": 0,
                "data": []
            }

        try:
            response = requests.get(
                self.url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=20
            )

            # -------------------------
            # SAFE JSON PARSE
            # -------------------------
            try:
                data = response.json()
            except Exception:
                return {
                    "type": "sales",
                    "status": "ERROR",
                    "error": "INVALID JSON RESPONSE",
                    "code": response.status_code,
                    "data": []
                }

            # -------------------------
            # SAFE RETURN
            # -------------------------
            return {
                "type": "sales",
                "status": "OK" if response.status_code == 200 else "ERROR",
                "code": response.status_code,
                "data": data.get("data", []) if isinstance(data, dict) else []
            }

        except Exception as e:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": str(e),
                "code": 0,
                "data": []
            }
