import os
import requests
from datetime import datetime

class APIConnector:

    def __init__(self):
        self.logs = []

        # ENV LOAD (SAFE)
        self.YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
        self.YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

        self.PINTEREST_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")

        self.SALES_API_KEY = os.getenv("SALES_API_KEY")
        self.SALES_API_URL = os.getenv("SALES_API_URL")

    # =========================
    # SAFE CHECK
    # =========================
    def is_available(self, value):
        return value is not None and value != ""

    # =========================
    # SALES API
    # =========================
    def send_sales_lead(self, product_id, source="api"):

        if not self.is_available(self.SALES_API_URL):
            return {"status": "SKIPPED_NO_SALES_API"}

        try:
            res = requests.post(
                self.SALES_API_URL,
                json={
                    "product_id": product_id,
                    "source": source,
                    "timestamp": datetime.utcnow().isoformat()
                },
                timeout=5
            )

            log = {
                "type": "sales",
                "status": "SENT",
                "code": res.status_code,
                "product_id": product_id
            }

        except Exception as e:
            log = {
                "type": "sales",
                "status": "FAILED",
                "error": str(e)
            }

        self.logs.append(log)
        return log

    # =========================
    # YOUTUBE (NO CRASH MODE)
    # =========================
    def upload_youtube_video(self, title, description):

        if not self.is_available(self.YOUTUBE_REFRESH_TOKEN):
            return {"status": "SKIPPED_NO_YOUTUBE_TOKEN"}

        log = {
            "type": "youtube",
            "title": title,
            "description": description,
            "status": "READY"
        }

        self.logs.append(log)
        return log

    # =========================
    # PINTEREST
    # =========================
    def create_pinterest_pin(self, title):

        if not self.is_available(self.PINTEREST_TOKEN):
            return {"status": "SKIPPED_NO_PINTEREST_TOKEN"}

        log = {
            "type": "pinterest",
            "title": title,
            "status": "READY"
        }

        self.logs.append(log)
        return log

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total_calls": len(self.logs),
            "last_logs": self.logs[-10:]
        }
