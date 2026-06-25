import os
import requests
from datetime import datetime


class APIConnector:

    def __init__(self):

        # =========================
        # ENV LOAD (SAFE)
        # =========================

        # YouTube / Google
        self.YT_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
        self.YT_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.YT_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

        # Pinterest
        self.PINTEREST_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")

        # Sales API
        self.SALES_API_KEY = os.getenv("SALES_API_KEY")
        self.SALES_API_URL = os.getenv("SALES_API_URL")

        # Blogger (Google)
        self.BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
        self.BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
        self.BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")
        self.BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID")

        self.logs = []

    # =========================
    # SAFE CHECK
    # =========================
    def _ok(self, value):
        return value is not None and value != ""

    # =========================
    # SALES API
    # =========================
    def send_sales_lead(self, product_id, source="api"):

        if not self._ok(self.SALES_API_URL):
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

            result = {
                "type": "sales",
                "status": "SENT",
                "code": res.status_code,
                "product_id": product_id
            }

        except Exception as e:
            result = {
                "type": "sales",
                "status": "FAILED",
                "error": str(e)
            }

        self.logs.append(result)
        return result

    # =========================
    # YOUTUBE (READY FOR REAL API)
    # =========================
    def upload_youtube_video(self, title, description):

        if not self._ok(self.YT_REFRESH_TOKEN):
            return {"status": "SKIPPED_NO_YOUTUBE_AUTH"}

        result = {
            "type": "youtube",
            "title": title,
            "description": description,
            "status": "READY_FOR_UPLOAD",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(result)
        return result

    # =========================
    # PINTEREST
    # =========================
    def create_pinterest_pin(self, title):

        if not self._ok(self.PINTEREST_TOKEN):
            return {"status": "SKIPPED_NO_PINTEREST_TOKEN"}

        result = {
            "type": "pinterest",
            "title": title,
            "status": "READY_FOR_PIN",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(result)
        return result

    # =========================
    # BLOGGER (GOOGLE)
    # =========================
    def post_blogger(self, title, content):

        if not self._ok(self.BLOGGER_REFRESH_TOKEN):
            return {"status": "SKIPPED_NO_BLOGGER_AUTH"}

        result = {
            "type": "blogger",
            "title": title,
            "content": content,
            "blog_id": self.BLOGGER_BLOG_ID,
            "status": "READY_FOR_POST",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(result)
        return result

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total_calls": len(self.logs),
            "last_logs": self.logs[-10:]
        }
