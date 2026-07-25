import requests


class MediaWikiClient:

    def __init__(
        self,
        base_url="https://de.wikipedia.org/w/api.php"
    ):
        self.base_url = base_url


    def search(
        self,
        query,
        limit=5
    ):

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": limit
        }

        response = requests.get(
            self.base_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


    def summary_ready(
        self,
        title
    ):

        return {
            "title": title,
            "status": "ready_for_enrichment",
            "source": "MediaWiki API"
        }


if __name__ == "__main__":

    client = MediaWikiClient()

    result = client.search(
        "DSL"
    )

    print(result)
