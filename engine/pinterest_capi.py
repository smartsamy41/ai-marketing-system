import os
import time
import uuid
import requests


class PinterestCAPI:

    def __init__(self):

        self.token = os.getenv(
            "PINTEREST_CAPI_ACCESS_TOKEN"
        )

        self.ad_account_id = os.getenv(
            "PINTEREST_AD_ACCOUNT_ID"
        )

        if not self.token:
            raise Exception(
                "Missing PINTEREST_CAPI_ACCESS_TOKEN"
            )

        if not self.ad_account_id:
            raise Exception(
                "Missing PINTEREST_AD_ACCOUNT_ID"
            )


    def send_event(
        self,
        event_name,
        event_source_url,
        custom_data=None
    ):

        url = (
            f"https://api.pinterest.com/v5/"
            f"ad_accounts/{self.ad_account_id}/events"
        )


        payload = {
            "data": [
                {
                    "event_name": event_name,
                    "event_time": int(time.time()),
                    "event_id": str(uuid.uuid4()),
                    "action_source": "web",
                    "event_source_url": event_source_url,
                    "custom_data": custom_data or {}
                }
            ]
        }


        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


        response = requests.post(
            url,
            headers=headers,
            json=payload
        )


        return {
            "status_code": response.status_code,
            "response": response.json()
            if response.text
            else {}
        }


    def page_visit(self, url):

        return self.send_event(
            "page_visit",
            url
        )


    def lead(
        self,
        url,
        product_id
    ):

        return self.send_event(
            "lead",
            url,
            {
                "content_ids": [
                    product_id
                ]
            }
        )


    def checkout(
        self,
        url,
        value,
        currency="EUR"
    ):

        return self.send_event(
            "checkout",
            url,
            {
                "value": value,
                "currency": currency
            }
        )
