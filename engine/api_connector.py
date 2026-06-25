import os
import requests
from requests.auth import HTTPBasicAuth


class APIConnector:

    def send_sales_lead(self, product_id):

        url = os.getenv(
            "TARIFCHECK_API_URL",
            "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"
        )

        username = os.getenv("TARIFCHECK_USERNAME")
        password = os.getenv("TARIFCHECK_PASSWORD")

        # ❗ SAFETY CHECK
        if not username or not password:
            return {
                "type": "sales",
                "status": "SKIPPED",
                "error": "Missing ENV credentials"
            }

        try:
            response = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                timeout=20
            )

            return {
                "type": "sales",
                "status": "OK",
                "code": response.status_code,
                "response": response.text[:200]
            }

        except Exception as e:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": str(e)
            }

    # placeholder
    def upload_youtube_video(self, title, description):
        return {"type": "youtube", "title": title, "status": "READY_FOR_GOOGLE_API"}

    def create_pinterest_pin(self, title):
        return {"type": "pinterest", "title": title, "status": "READY_FOR_PIN"}

    def report(self):
        return {"status": "OK"}
