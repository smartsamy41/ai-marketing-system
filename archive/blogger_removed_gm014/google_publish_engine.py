import traceback
from datetime import datetime

from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GooglePublishEngine:

    def __init__(self):

        # =========================
        # CLOUD RUN SAFE AUTH
        # =========================
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/blogger"
        ]

        self.creds, _ = default(scopes=self.scopes)

        # =========================
        # API CLIENTS
        # =========================
        self.youtube = build("youtube", "v3", credentials=self.creds)
        self.blogger = build("blogger", "v3", credentials=self.creds)

    # =========================
    # BLOGGER PUBLISH (REAL)
    # =========================
    def publish_blogger(self, blog_id, title, html_content):

        try:

            body = {
                "title": title,
                "content": html_content
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
    # YOUTUBE UPLOAD (REAL)
    # =========================
    def publish_youtube(self, video_file, title, description="Auto generated video"):

        try:

            media = MediaFileUpload(video_file, resumable=True)

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
            }
