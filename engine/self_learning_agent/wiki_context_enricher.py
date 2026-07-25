class WikiContextEnricher:

    def __init__(
        self,
        source="mediawiki_wikidata"
    ):

        self.source = source


    def enrich(
        self,
        entity,
        context=None
    ):

        return {
            "entity": entity,
            "context": context or {},
            "source": self.source,
            "status": "enriched_ready"
        }


    def attach_reference(
        self,
        title,
        url
    ):

        return {
            "title": title,
            "reference": url,
            "type": "knowledge_source"
        }


if __name__ == "__main__":

    enricher = WikiContextEnricher()

    print(
        enricher.enrich(
            "DSL"
        )
    )
