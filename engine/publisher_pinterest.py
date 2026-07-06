import requests
import os

class PinterestPublisher:

    def __init__(self, access_token: str, board_id: str):

        self.access_token = access_token
        self.board_id = board_id

    # =========================
    # REAL PINTEREST PUBLISH
    # =========================
    def publish(self, content, image_url: str, link: str):

        url = "https://api.pinterest.com/v5/pins"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "board_id": self.board_id,
            "title": content.get("title"),
            "description": content.get("description", ""),
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code not in [200, 201]:
            return {
                "status": "error",
                "code": response.status_code,
                "response": response.text
            }

        return {
            "status": "published",
            "platform": "pinterest",
            "data": response.json()
        }
