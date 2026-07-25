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
            "Accept": "application/sparql-results+json"
        }

        response = requests.get(
            self.endpoint,
            params={
                "query": sparql_query,
                "format": "json"
            },
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        return response.json()


    def entity_lookup(
        self,
        label
    ):

        query = f"""
        SELECT ?item ?itemLabel WHERE {{
          ?item rdfs:label "{label}"@de.
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "de".
          }}
        }}
        LIMIT 5
        """

        return self.query(query)


if __name__ == "__main__":

    client = WikidataClient()

    result = client.entity_lookup(
        "DSL"
    )

    print(result)
