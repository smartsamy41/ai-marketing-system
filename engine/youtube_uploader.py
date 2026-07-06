from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:

    def __init__(self, youtube_client):

        self.youtube = youtube_client

    def upload(self, file_path: str, title: str, description: str):

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=MediaFileUpload(file_path)
        )

        return request.execute()
