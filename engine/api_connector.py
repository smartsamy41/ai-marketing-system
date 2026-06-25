import os
import requests
from datetime import datetime


class APIConnector:

    def __init__(self):

        # =========================
        # LOAD ENV (CLEAN)
        # =========================

        # YouTube
        self.yt_client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.yt_client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.yt_refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

        # Pinterest
        self.pinterest_token = os.getenv("PINTEREST_ACCESS_TOKEN")

        # Sales API (Tarifcheck)
        self.sales_url = os.getenv("SALES_API_URL")
        self.sales_key = os.getenv("SALES_API_KEY")

        # Blogger
        self.blogger_client_id = os.getenv("BLOGGER_CLIENT_ID")
        self.blogger_client_secret = os.getenv("BLOGGER_CLIENT_SECRET")
        self.blogger_refresh_token = os.getenv("BLOGGER_REFRESH_TOKEN")
        self.blogger_blog_id = os.getenv("BLOGGER_BLOG_ID")

        self.logs = []

    # =========================
    # SAFE CHECK
    # =========================
    def _ok(self, v):
        return v is not None and v != ""

    # =========================
    # SALES API (REAL FIX)
    # =========================
    def send_sales_lead(self, product_id, source="api"):

        if not self._ok(self.sales_url):
            return {"status": "SKIPPED_NO_SALES_URL"}

        try:
            response = requests.post(
                self.sales_url,
                json={
                    "product_id": product_id,
                    "source": source,
                    "timestamp": datetime.utcnow().isoformat()
                },
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
    # YOUTUBE (READY MODE)
    # =========================
    def upload_youtube_video(self, title, description):

        if not self._ok(self.yt_refresh_token):
            return {"status": "SKIPPED_NO_YOUTUBE_TOKEN"}

        return {
            "type": "youtube",
            "title": title,
            "description": description,
            "status": "READY_FOR_GOOGLE_API",
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # PINTEREST
    # =========================
    def create_pinterest_pin(self, title):

        if not self._ok(self.pinterest_token):
            return {"status": "SKIPPED_NO_PINTEREST_TOKEN"}

        return {
            "type": "pinterest",
            "title": title,
            "status": "READY_FOR_PIN",
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # BLOGGER
    # =========================
    def post_blogger(self, title, content):

        if not self._ok(self.blogger_refresh_token):
            return {"status": "SKIPPED_NO_BLOGGER_TOKEN"}

        return {
            "type": "blogger",
            "title": title,
            "content": content,
            "blog_id": self.blogger_blog_id,
            "status": "READY_FOR_POST",
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "logs_count": len(self.logs),
            "last_logs": self.logs[-10:]
        }
