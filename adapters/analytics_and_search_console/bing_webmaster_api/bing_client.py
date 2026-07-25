class BingWebmasterClient:

    def __init__(
        self,
        site_url=None,
        api_key=None
    ):

        self.site_url = site_url
        self.api_key = api_key


    def get_search_data(
        self
    ):

        return {
            "site_url": self.site_url,
            "status": "ready_for_api_connection",
            "data": []
        }


    def analyze_keyword(
        self,
        keyword
    ):

        return {
            "keyword": keyword,
            "status": "pending_bing_data"
        }


if __name__ == "__main__":

    client = BingWebmasterClient(
        "https://freebasics.online"
    )

    print(
        client.get_search_data()
    )
