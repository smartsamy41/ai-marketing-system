import os
import requests
from requests.auth import HTTPBasicAuth


class APIConnector:

    # =========================
    # SALES API (CLEAN OUTPUT FIX)
    # =========================
    def send_sales_lead(self, product_id):

        url = os.getenv("TARIFCHECK_API_URL")
        username = os.getenv("TARIFCHECK_USERNAME")
        password = os.getenv("TARIFCHECK_PASSWORD")

        # =========================
        # DEBUG (SAFE)
        # =========================
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
            response = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                timeout=20
            )

            # =========================
            # CLEAN JSON PARSING (NO DOUBLE ENCODING)
            # =========================
            try:
                data = response.json()
            except Exception:
                return {
                    "type": "sales",
                    "status": "ERROR",
                    "error": "Invalid JSON response",
                    "raw": response.text[:200]
                }

            # =========================
            # CLEAN STRUCTURE OUTPUT
            # =========================
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
    # YOUTUBE (PLACEHOLDER SAFE)
    # =========================
    def upload_youtube_video(self, title, description):
        return {
            "type": "youtube",
            "status": "READY_FOR_GOOGLE_API",
            "title": title,
            "description": description
        }

    # =========================
    # PINTEREST (PLACEHOLDER SAFE)
    # =========================
    def create_pinterest_pin(self, title):
        return {
            "type": "pinterest",
            "status": "READY_FOR_PIN",
            "title": title
        }

    # =========================
    # REPORT
    # =========================
    def report(self):
        return {
            "status": "OK",
            "system": "CLEAN OUTPUT LAYER V1"
        }
