import os
import requests


# =========================
# YOUTUBE CONNECTOR (FULL)
# =========================
class YouTubeConnector:

    def __init__(self):
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    def upload_video(self, title, description):

        # DEBUG
        if not self.client_id or not self.refresh_token:
            return {
                "status": "ERROR",
                "message": "Missing YouTube ENV credentials"
            }

        # REAL PLACEHOLDER API FLOW
        return {
            "status": "READY_FOR_REAL_UPLOAD",
            "platform": "youtube",
            "title": title,
            "description": description
        }


# =========================
# PINTEREST CONNECTOR (FULL)
# =========================
class PinterestConnector:

    def __init__(self):
        self.token = os.getenv("PINTEREST_ACCESS_TOKEN")

    def create_pin(self, title):

        if not self.token:
            return {
                "status": "ERROR",
                "message": "Missing Pinterest Token"
            }

        return {
            "status": "READY_FOR_REAL_PIN",
            "platform": "pinterest",
            "title": title
        }


# =========================
# BLOGGER CONNECTOR (FULL)
# =========================
class BloggerConnector:

    def __init__(self):
        self.client_id = os.getenv("BLOGGER_CLIENT_ID")
        self.client_secret = os.getenv("BLOGGER_CLIENT_SECRET")
        self.refresh_token = os.getenv("BLOGGER_REFRESH_TOKEN")
        self.blog_id = os.getenv("BLOGGER_BLOG_ID")

    def publish_post(self, title, content):

        if not self.blog_id:
            return {
                "status": "ERROR",
                "message": "Missing Blogger BLOG_ID"
            }

        return {
            "status": "READY_FOR_REAL_POST",
            "platform": "blogger",
            "title": title,
            "content": content
        }


# =========================
# SALES CONNECTOR (TARIFCHECK)
# =========================
class SalesConnector:

    def __init__(self):
        self.username = os.getenv("TARIFCHECK_USERNAME")
        self.password = os.getenv("TARIFCHECK_PASSWORD")
        self.url = os.getenv(
            "TARIFCHECK_API_URL",
            "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"
        )

    def fetch_leads(self):

        if not self.username or not self.password:
            return {
                "status": "ERROR",
                "message": "Missing Sales ENV credentials"
            }

        try:
            response = requests.get(
                self.url,
                auth=(self.username, self.password),
                timeout=20
            )

            return {
                "status": "OK",
                "code": response.status_code,
                "data": response.json().get("data", [])
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }


# =========================
# OUTPUT ENGINE WRAPPER
# =========================
class OutputEngine:

    def __init__(self):
        self.youtube = YouTubeConnector()
        self.pinterest = PinterestConnector()
        self.blogger = BloggerConnector()

    def publish_all(self, product_id):

        yt = self.youtube.upload_video(
            title=f"{product_id} Vergleich 2026",
            description="Auto Content"
        )

        pin = self.pinterest.create_pin(
            title=f"{product_id} sparen & vergleichen"
        )

        blog = self.blogger.publish_post(
            title=f"{product_id} Review 2026",
            content="Auto Content"
        )

        return {
            "youtube": yt,
            "pinterest": pin,
            "blogger": blog
        }
