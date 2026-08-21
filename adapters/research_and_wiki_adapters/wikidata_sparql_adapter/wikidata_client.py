import requests


class WikidataClient:

    def __init__(
        self,
        endpoint="https://query.wikidata.org/sparql"
    ):

        self.endpoint = endpoint


    def query(
        self,
        sparql_query
    ):

        headers = {
            "Accept": "application/sparql-results+json",
            "User-Agent": (
                "FreeBasicsAI/1.0 "
                "(https://freebasics.online)"
            )
        }


        response = requests.get(

            self.endpoint,

            params={
                "query": sparql_query,
                "format": "json"
            },

            headers=headers,

            timeout=30

        )


        response.raise_for_status()

        return response.json()


    def entity_lookup(
        self,
        label
    ):

        safe_label = str(
            label
        ).replace(
            '"',
            '\\"'
        )


        query = f"""
        SELECT ?item ?itemLabel WHERE {{

          ?item rdfs:label "{safe_label}"@de.

          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "de".
          }}

        }}

        LIMIT 5
        """


        return self.query(
            query
        )


    def german_location_lookup(
        self,
        name
    ):

        safe_name = str(
            name
        ).replace(
            '"',
            '\\"'
        )


        query = f"""
        SELECT DISTINCT
            ?item
            ?itemLabel
            ?state
            ?stateLabel
            ?postalCode
            ?coordinate

        WHERE {{

          ?item rdfs:label "{safe_name}"@de.

          ?item wdt:P17 wd:Q183.

          OPTIONAL {{
            ?item wdt:P131 ?state.
          }}

          OPTIONAL {{
            ?item wdt:P281 ?postalCode.
          }}

          OPTIONAL {{
            ?item wdt:P625 ?coordinate.
          }}

          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "de".
          }}

        }}

        LIMIT 20
        """


        return self.query(
            query
        )


    @staticmethod
    def parse_qid(
        uri
    ):

        if not uri:
            return ""

        return str(
            uri
        ).rstrip(
            "/"
        ).split(
            "/"
        )[-1]


    def normalized_location_lookup(
        self,
        name
    ):

        raw = self.german_location_lookup(
            name
        )


        bindings = (
            raw
            .get("results", {})
            .get("bindings", [])
        )


        results = []


        for row in bindings:

            item_uri = (
                row
                .get("item", {})
                .get("value", "")
            )

            state_uri = (
                row
                .get("state", {})
                .get("value", "")
            )


            results.append(
                {
                    "name":
                        (
                            row
                            .get("itemLabel", {})
                            .get(
                                "value",
                                name
                            )
                        ),

                    "wikidata_id":
                        self.parse_qid(
                            item_uri
                        ),

                    "wikidata_url":
                        item_uri,

                    "state":
                        (
                            row
                            .get("stateLabel", {})
                            .get(
                                "value",
                                ""
                            )
                        ),

                    "state_wikidata_id":
                        self.parse_qid(
                            state_uri
                        ),

                    "postal_code":
                        (
                            row
                            .get("postalCode", {})
                            .get(
                                "value",
                                ""
                            )
                        ),

                    "coordinate":
                        (
                            row
                            .get("coordinate", {})
                            .get(
                                "value",
                                ""
                            )
                        ),

                    "country":
                        "Deutschland",

                    "source":
                        "Wikidata SPARQL",

                    "real_location":
                        bool(
                            item_uri
                        ),

                    "source_verified":
                        bool(
                            item_uri
                        ),

                    "wikidata_verified":
                        bool(
                            item_uri
                        )
                }
            )


        return results


if __name__ == "__main__":

    client = WikidataClient()

    result = client.normalized_location_lookup(
        "Lübeck"
    )

    for item in result:
        print(item)
