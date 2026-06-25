import os
import requests
from requests.auth import HTTPBasicAuth


class APIConnector:

    # =========================
    # TARIFCHECK SALES API
    # =========================
    def send_sales_lead(self, product_id):

        url = os.getenv("TARIFCHECK_API_URL")
        username = os.getenv("TARIFCHECK_USERNAME")
        password = os.getenv("TARIFCHECK_PASSWORD")

        # 🔥 DEBUG (hilft dir sofort Fehler zu sehen)
        print("=== SALES DEBUG ===")
        print("URL:", url)
        print("USERNAME:", username)
        print("PASSWORD:", "SET" if password else "MISSING")

        # =========================
        # ENV CHECK
        # =========================
        if not url or not username or not password:
            return {
                "type": "sales",
                "status": "SKIPPED",
                "error": "Missing ENV credentials"
            }

        try:
            # =========================
            # REAL API CALL
            # =========================
            response = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                timeout=20
            )

            # =========================
            # SAFE JSON PARSE
            # =========================
            try:
                data = response.json()
            except:
                return {
                    "type": "sales",
                    "status": "ERROR",
                    "error": "Invalid JSON response",
                    "raw": response.text[:200]
                }

            return {
                "type": "sales",
                "status": "OK",
                "code": response.status_code,
                "data": data.get("data", [])
            }

        except Exception as e:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": str(e)
            }

    # =========================
    # PLACEHOLDER MODULES
    # =========================

    def upload_youtube_video(self, title, description):
        return {
            "type": "youtube",
            "status": "READY_FOR_GOOGLE_API",
            "title": title,
            "description": description
        }

    def create_pinterest_pin(self, title):
        return {
            "type": "pinterest",
            "status": "READY_FOR_PIN",
            "title": title
        }

    def report(self):
        return {
            "status": "OK",
            "system": "API CONNECTOR V2"
        }
