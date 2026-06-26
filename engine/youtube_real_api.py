import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials


class YouTubeRealAPI:

    def __init__(self):

        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.token = os.getenv("YOUTUBE_TOKEN_JSON")

        self.channel = os.getenv("YOUTUBE_CHANNEL", "freebasics_online")

        self.service = None

    # =========================
    # AUTH (SAFE INIT)
    # =========================
    def authenticate(self):

        # NOTE: später OAuth Flow ersetzen
        creds = Credentials(token=self.token)

        self.service = build("youtube", "v3", credentials=creds)

        return {"status": "AUTH_READY"}

    # =========================
    # UPLOAD VIDEO
    # =========================
    def upload_video(self, file_path, title, description):

        if not self.service:
            self.authenticate()

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        media = MediaFileUpload(file_path, resumable=True)

        request = self.service.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )

        response = request.execute()

        return {
            "status": "UPLOADED",
            "video_id": response.get("id")
        }
