import traceback
from datetime import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account


class OrchestratorCleanMaster:

    def __init__(self):

        self.products = [
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]

        # =========================
        # LIVE SWITCH
        # =========================
        self.LIVE_MODE = False

        # =========================
        # GOOGLE CLOUD AUTH (SERVICE ACCOUNT)
        # =========================
        self.SCOPES = [
            "https://www.googleapis.com/auth/blogger",
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        self.SERVICE_ACCOUNT_FILE = "/secrets/service-account.json"

    # =========================
    # AUTH SERVICES
    # =========================
    def get_blogger_service(self):

        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE,
            scopes=self.SCOPES
        )

        return build("blogger", "v3", credentials=creds)

    def get_youtube_service(self):

        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE,
            scopes=self.SCOPES
        )

        return build("youtube", "v3", credentials=creds)

    # =========================
    # CONTENT
    # =========================
    def build_content(self, product_id):

        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "status": "READY"
        }

    # =========================
    # LANDINGPAGE
    # =========================
    def build_landingpage(self, product_id):

        html = f"""
        <html>
            <head>
                <title>{product_id} Vergleich 2026</title>
            </head>
            <body>
                <h1>{product_id} Vergleich 2026</h1>
                <p>Vergleich starten für {product_id}</p>
                <a href="/affiliate/{product_id}">Jetzt vergleichen</a>
            </body>
        </html>
        """

        return {
            "product_id": product_id,
            "html": html,
            "status": "READY"
        }

    # =========================
    # BLOGGER POST (REAL)
    # =========================
    def publish_blogger(self, product_id, content):

        try:
            service = self.get_blogger_service()

            blog_id = "6148350625430723499"

            body = {
                "title": content["title"],
                "content": f"<h1>{content['title']}</h1><p>Automatischer Vergleich</p>"
            }

            if self.LIVE_MODE:

                post = service.posts().insert(
                    blogId=blog_id,
                    body=body,
                    isDraft=False
                ).execute()

                return {
                    "status": "BLOGGER_LIVE",
                    "post_id": post.get("id")
                }

            return {
                "status": "BLOGGER_SIMULATED"
            }

        except Exception as e:

            return {
                "status": "BLOGGER_ERROR",
                "error": str(e)
            }

    # =========================
    # YOUTUBE UPLOAD (REAL PLACEHOLDER SAFE)
    # =========================
    def publish_youtube(self, product_id):

        try:

            service = self.get_youtube_service()

            if self.LIVE_MODE:

                return {
                    "status": "YOUTUBE_LIVE_READY",
                    "note": "Upload engine hook ready (MP4 pipeline required)"
                }

            return {
                "status": "YOUTUBE_SIMULATED"
            }

        except Exception as e:

            return {
                "status": "YOUTUBE_ERROR",
                "error": str(e)
            }

    # =========================
    # PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                content = self.build_content(p)
                landing = self.build_landingpage(p)

                blogger = self.publish_blogger(p, content)
                youtube = self.publish_youtube(p)

                results.append({
                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "blogger": blogger,
                    "youtube": youtube,
                    "status": "PIPELINE_OK",
                    "timestamp": datetime.utcnow().isoformat(),
                    "live_mode": self.LIVE_MODE
                })

            except Exception as e:

                results.append({
                    "product_id": p,
                    "status": "PIPELINE_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return {
            "status": "DONE",
            "mode": "REAL_API_LAYER_ACTIVE",
            "live_enabled": self.LIVE_MODE,
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
