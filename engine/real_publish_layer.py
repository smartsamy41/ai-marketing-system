import os


class RealPublishLayer:

    # ============from datetime import datetime
import traceback

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth import default


class RealPublishLayer:

    def __init__(self):

        # =========================
        # GOOGLE AUTH (CLOUD RUN SAFE)
        # =========================
        self.scopes = [
            "https://www.googleapis.com/auth/blogger",
            "https://www.googleapis.com/auth/youtube.upload"
        ]

        self.creds, _ = default(scopes=self.scopes)

        self.youtube = build("youtube", "v3", credentials=self.creds)
        self.blogger = build("blogger", "v3", credentials=self.creds)

    # =========================
    # BLOGGER POST REAL
    # =========================
    def publish_blogger(self, blog_id, title, content):

        try:

            body = {
                "title": title,
                "content": content
            }

            request = self.blogger.posts().insert(
                blogId=blog_id,
                body=body
            )

            response = request.execute()

            return {
                "status": "BLOGGER_PUBLISHED",
                "post_id": response.get("id"),
                "url": response.get("url"),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:

            return {
                "status": "BLOGGER_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

    # =========================
    # YOUTUBE UPLOAD REAL
    # =========================
    def publish_youtube(self, video_file, title, description="Auto generated video"):

        try:

            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)

            request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "categoryId": "22"
                    },
                    "status": {
                        "privacyStatus": "unlisted"
                    }
                },
                media_body=media
            )

            response = request.execute()

            return {
                "status": "YOUTUBE_UPLOADED",
                "video_id": response.get("id"),
                "url": f"https://www.youtube.com/watch?v={response.get('id')}",
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:

            return {
                "status": "YOUTUBE_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }=============
    # BLOGGER PUBLISH (SAFE STRUCTURE)
    # =========================
    def publish_to_blogger(self, product_id, content):

        blog_id = os.getenv("BLOGGER_BLOG_ID")

        return {
            "platform": "blogger",
            "blog_id": blog_id,
            "product_id": product_id,
            "title": content.get("title"),
            "status": "READY_TO_PUBLISH",
            "action": "CREATE_POST"
        }

    # =========================
    # PINTEREST QUEUE
    # =========================
    def publish_to_pinterest(self, product_id, content):

        return {
            "platform": "pinterest",
            "product_id": product_id,
            "title": content.get("title"),
            "status": "QUEUED",
            "action": "CREATE_PIN"
        }

    # =========================
    # YOUTUBE OUTPUT (NO UPLOAD YET SAFE)
    # =========================
    def publish_to_youtube(self, product_id, content):

        return {
            "platform": "youtube",
            "product_id": product_id,
            "title": content.get("title"),
            "status": "SCRIPT_READY",
            "action": "VIDEO_SCRIPT_ONLY"
        }

    # =========================
    # MASTER PUBLISH FUNCTION
    # =========================
    def publish_all(self, product_id, content):

        return {
            "product_id": product_id,

            "blogger": self.publish_to_blogger(product_id, content),
            "pinterest": self.publish_to_pinterest(product_id, content),
            "youtube": self.publish_to_youtube(product_id, content),

            "status": "REAL_PUBLISH_LAYER_ACTIVE"
        }
