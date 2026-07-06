import requests

class PinterestReal:

    def __init__(self, access_token):

        self.token = access_token

    # =========================
    # CREATE PIN
    # =========================
    def create_pin(self, board_id, title, description, link, image_url):

        url = "https://api.pinterest.com/v5/pins"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "board_id": board_id,
            "title": title,
            "description": description,
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()
