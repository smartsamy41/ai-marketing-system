import requests

class PinterestUploader:

    def __init__(self, token: str):

        self.token = token

    def create_pin(self, board_id, title, link, image_url):

        url = "https://api.pinterest.com/v5/pins"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "board_id": board_id,
            "title": title,
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        return requests.post(url, json=data, headers=headers).json()
