import os
import requests
from requests.auth import HTTPBasicAuth


class APIConnector:

    # =========================
    # TARIFCHECK SALES
    # =========================
    def send_sales_lead(self, product_id):

        url = os.getenv("TARIFCHECK_API_URL")
        username = os.getenv("TARIFCHECK_USERNAME")
        password = os.getenv("TARIFCHECK_PASSWORD")

        # 🔥 DEBUG (WICHTIG)
        print("DEBUG USER:", username)
        print("DEBUG PASS:", "SET" if password else "MISSING")
        print("DEBUG URL:", url)

        # safety check
        if not url or not username or not password:
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

    # =========================
    # PLACEHOLDERS
    # =========================
    def upload_youtube_video(self, title, description):
        return {"type": "youtube", "status": "READY"}

    def create_pinterest_pin(self, title):
        return {"type": "pinterest", "status": "READY"}

    def report(self):
        return {"status": "OK"}
