import os
import requests
from datetime import datetime

# =========================
# ENV LOAD (CLOUD SAFE)
# =========================

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

PINTEREST_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")

SALES_API_URL = os.getenv("SALES_API_URL")
SALES_API_KEY = os.getenv("SALES_API_KEY")


# =========================
# API CONNECTOR CLASS
# =========================

class APIConnector:

    def __init__(self):
        self.logs = []

    # =========================
    # YOUTUBE ACCESS TOKEN
    # =========================
    def get_youtube_access_token(self):

        if not YOUTUBE_REFRESH_TOKEN:
            return None

        url = "https://oauth2.googleapis.com/token"

        payload = {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "refresh_token": YOUTUBE_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }

        try:
            res = requests.post(url, data=payload, timeout=10)
            return res.json().get("access_token")

        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    # =========================
    # YOUTUBE VIDEO UPLOAD (STRUCTURE READY)
    # =========================
    def upload_youtube_video(self, title, description):

        token = self.get_youtube_access_token()

        log = {
            "platform": "youtube",
            "title": title,
            "description": description,
            "token_active": bool(token),
            "status": "READY_FOR_UPLOAD",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)
        return log

    # =========================
    # PINTEREST PIN CREATE
    # =========================
    def create_pinterest_pin(self, title, board_id="default"):

        if not PINTEREST_TOKEN:
            return {
                "status": "ERROR",
                "reason": "NO_PINTEREST_TOKEN"
            }

        payload = {
            "title": title,
            "board_id": board_id,
            "description": "Auto generated pin"
        }

        log = {
            "platform": "pinterest",
            "title": title,
            "status": "READY_FOR_POST",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)
        return log

    # =========================
    # SALES API (REAL CONNECT)
    # =========================
    def send_sales_lead(self, product_id, source="api"):

        if not SALES_API_URL:
            return {
                "status": "ERROR",
                "reason": "NO_SALES_API_URL"
            }

        payload = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        headers = {
            "Authorization": f"Bearer {SALES_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            res = requests.post(
                SALES_API_URL,
                json=payload,
                headers=headers,
                timeout=10
            )

            log = {
                "platform": "sales",
                "product_id": product_id,
                "status_code": res.status_code,
                "status": "SENT",
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:

            log = {
                "platform": "sales",
                "product_id": product_id,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

        self.logs.append(log)
        return log

    # =========================
    # SYSTEM REPORT
    # =========================
    def report(self):

        return {
            "total_requests": len(self.logs),
            "last_logs": self.logs[-10:] if self.logs else [],
            "timestamp": datetime.utcnow().isoformat()
        }
