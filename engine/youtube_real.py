from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

class YouTubeReal:

    def __init__(self, credentials):

        self.youtube = build("youtube", "v3", credentials=credentials)

    # =========================
    # UPLOAD VIDEO
    # =========================
    def upload_video(self, file_path, title, description):

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            media_body=MediaFileUpload(file_path)
        )

        response = request.execute()

        return response
