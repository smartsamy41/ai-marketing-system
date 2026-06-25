import os
import requests
from requests.auth import HTTPBasicAuth


class APIConnector:

    # =========================
    # SALES API (CLEAN + NO STRING WRAP)
    # =========================
    def send_sales_lead(self, product_id):

        url = os.getenv("TARIFCHECK_API_URL")
        username = os.getenv("TARIFCHECK_USERNAME")
        password = os.getenv("TARIFCHECK_PASSWORD")

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

            # 🟢 IMPORTANT: ONLY ONCE JSON PARSING
            data = response.json()

            return {
                "type": "sales",
                "status": "OK",
                "code": response.status_code,

                # 🔥 CLEAN OUTPUT (NO STRING INSIDE STRING)
                "data": data.get("data", [])
            }

        except Exception as e:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": str(e)
            }

    # =========================
    # YOUTUBE (PLACEHOLDER)
    # =========================
    def upload_youtube_video(self, title, description):
        return {
            "type": "youtube",
            "status": "READY",
            "title": title,
            "description": description
        }

    # =========================
    # PINTEREST (PLACEHOLDER)
    # =========================
    def create_pinterest_pin(self, title):
        return {
            "type": "pinterest",
            "status": "READY",
            "title": title
        }

    # =========================
    # REPORT
    # =========================
    def report(self):
        return {
            "status": "OK",
            "system": "CLEAN PIPELINE V2"
        }
