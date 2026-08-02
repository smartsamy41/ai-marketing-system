from google.cloud import secretmanager
import requests


class BingWebmasterClient:


    def __init__(
        self,
        site_url=None
    ):

        self.site_url = (
            site_url
            or "https://freebasics.online"
        )



    def _get_api_key(self):

        client = secretmanager.SecretManagerServiceClient()

        key = client.access_secret_version(
            request={
                "name":
                "projects/smartcontent2050/secrets/BING_WEBMASTER_API_KEY/versions/latest"
            }
        ).payload.data.decode().strip()

        return key



    def get_search_data(
        self
    ):

        key = self._get_api_key()


        url = (
            "https://ssl.bing.com/webmaster/api.svc/json/"
            "GetRankAndTrafficStats"
        )


        response = requests.get(

            url,

            params={

                "siteUrl":
                    self.site_url,

                "apikey":
                    key

            },

            timeout=30

        )


        response.raise_for_status()


        data = response.json()


        rows = []


        for item in data.get(
            "d",
            []
        ):

            rows.append({

                "clicks":
                    item.get(
                        "Clicks",
                        0
                    ),

                "impressions":
                    item.get(
                        "Impressions",
                        0
                    )

            })


        return {

            "site_url":
                self.site_url,

            "status":
                "LIVE",

            "rows":
                rows

        }



if __name__ == "__main__":


    client = BingWebmasterClient(
        "https://freebasics.online"
    )


    print(
        client.get_search_data()
    )
