class KeywordDiscoveryEngine:

    def __init__(
        self,
        source="search_data"
    ):

        self.source = source


    def discover(
        self,
        queries
    ):

        keywords = []

        for query in queries:

            keywords.append(
                {
                    "keyword": query.get("query"),
                    "clicks": query.get("clicks", 0),
                    "impressions": query.get("impressions", 0),
                    "status": "discovered"
                }
            )

        return {
            "source": self.source,
            "keywords": keywords,
            "count": len(keywords)
        }


    def detect_content_gap(
        self,
        keyword
    ):

        return {
            "keyword": keyword,
            "content_needed": True,
            "status": "candidate"
        }


if __name__ == "__main__":

    engine = KeywordDiscoveryEngine()

    print(
        engine.discover(
            [
                {
                    "query": "DSL Vergleich",
                    "clicks": 10,
                    "impressions": 100
                }
            ]
        )
    )
