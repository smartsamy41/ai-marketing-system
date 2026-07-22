import os
import time
import requests


class TikTokTracking:

    def __init__(self):

        self.pixel_id = os.getenv(
            "TIKTOK_PIXEL_ID",
            ""
        )

        self.access_token = os.getenv(
            "TIKTOK_EVENTS_API_TOKEN",
            ""
        )

        self.endpoint = (
            "https://business-api.tiktok.com"
            "/open_api/v1.3/event/track/"
        )


    def send_event(
        self,
        event_name: str,
        url: str,
        content_id: str = "",
        content_name: str = "",
        value: float = 0,
        currency: str = "EUR"
    ):

        if not self.pixel_id or not self.access_token:
            return {
                "status": "missing_credentials"
            }


        payload = {
            "event_source": "web",
            "event_source_id": self.pixel_id,
            "data": [
                {
                    "event": event_name,
                    "event_time": int(time.time()),
                    "event_id": f"{event_name}_{int(time.time())}",
                    "properties": {
                        "content_id": content_id,
                        "content_name": content_name,
                        "content_type": "product",
                        "value": value,
                        "currency": currency,
                        "url": url
                    }
                }
            ]
        }


        headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }


        response = requests.post(
            self.endpoint,
            json=payload,
            headers=headers,
            timeout=10
        )


        return {
            "status_code": response.status_code,
            "response": response.text
        }


    def view_content(
        self,
        url,
        product_id="",
        product_name=""
    ):
        return self.send_event(
            "ViewContent",
            url,
            product_id,
            product_name
        )


    def click_button(
        self,
        url,
        product_id="",
        product_name=""
    ):
        return self.send_event(
            "ClickButton",
            url,
            product_id,
            product_name
        )


    def lead(
        self,
        url,
        product_id="",
        product_name=""
    ):
        return self.send_event(
            "Lead",
            url,
            product_id,
            product_name
        )
