import json
from pathlib import Path
from datetime import datetime, timezone


class AuthoritySourceGraphBuilder:


    def __init__(self):

        self.product_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.entity_file = Path(
            "data_master/geo_and_entities/entity_registry/entity_relationships.json"
        )

        self.source_file = Path(
            "data_master/source_layer/knowledge_sources.json"
        )

        self.primary_source_file = Path(
            "data_master/geo_and_entities/primary_sources_index.json"
        )

        self.backlink_file = Path(
            "data_master/authority_layer/backlink_registry.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )


    def load(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)



    def save(self, path, data):

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )



    def clean(self, value):

        if value is None:
            return ""

        return str(value).strip()



    def build(self):


        products = self.load(
            self.product_file
        )

        entities = self.load(
            self.entity_file
        )

        sources = self.load(
            self.source_file
        )

        primary_sources = self.load(
            self.primary_source_file
        )

        backlinks = self.load(
            self.backlink_file
        )

        articles = self.load(
            self.article_file
        )



        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "authority_source_graph",

            "version":
                "3.0",

            "status":
                "ACTIVE",


            "rules":
            {

                "verified_sources_only":
                    True,

                "source_required_for_claims":
                    True,

                "no_fabricated_sources":
                    True,

                "verified_backlinks_only":
                    True,

                "active_registry_only":
                    True

            },


            "connections":
            {

                "product_to_source": [],

                "entity_to_source": [],

                "article_to_source": [],

                "partner_to_source": [],

                "verified_backlinks": []

            },


            "validation":
            {

                "products_checked":0,

                "sources_found":0,

                "backlinks_checked":0,

                "verified_backlinks":0,

                "backlink_domains":0

            },

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }



        # SOURCES

        source_names = set()


        for item in sources.get(
            "sources",
            []
        ):

            name = item.get(
                "name"
            )

            if name:
                source_names.add(name)



        for item in primary_sources.get(
            "sources",
            []
        ):

            name = item.get(
                "name"
            )

            if name:
                source_names.add(name)



        graph["validation"]["sources_found"] = len(
            source_names
        )



        # PRODUCTS

        for product in products.get(
            "products",
            []
        ):

            product_id = product.get(
                "product_id"
            )

            if not product_id:
                continue


            graph["validation"]["products_checked"] += 1


            partner = product.get(
                "identity",
                {}
            ).get(
                "partner",
                ""
            )


            source = product.get(
                "knowledge",
                {}
            ).get(
                "llm_context",
                {}
            ).get(
                "source_reference",
                ""
            )


            source = source or partner


            if source:

                graph["connections"]["product_to_source"].append(
                    {
                        "product_id": product_id,
                        "source": source
                    }
                )


                if partner:

                    graph["connections"]["partner_to_source"].append(
                        {
                            "partner": partner,
                            "product_id": product_id
                        }
                    )



        # ENTITIES

        for relation in entities.get(
            "relationships",
            []
        ):

            entity = relation.get(
                "to_entity"
            )

            source = relation.get(
                "source"
            )


            if entity and source:

                graph["connections"]["entity_to_source"].append(
                    {
                        "entity": entity,
                        "source": source
                    }
                )



        # ARTICLES

        for article in articles.get(
            "articles",
            []
        ):

            product_id = article.get(
                "product_id"
            )

            for item in graph["connections"]["product_to_source"]:

                if item["product_id"] == product_id:

                    graph["connections"]["article_to_source"].append(
                        {
                            "product_id": product_id,
                            "source": item["source"]
                        }
                    )



        # VERIFIED BACKLINKS

        domains = set()


        for backlink in backlinks.get(
            "backlinks",
            []
        ):


            graph["validation"]["backlinks_checked"] += 1


            if backlink.get(
                "status",
                ""
            ).upper() != "ACTIVE":

                continue


            source_url = self.clean(
                backlink.get("source_url")
            )

            source_domain = self.clean(
                backlink.get("source_domain")
            )

            target_url = self.clean(
                backlink.get("target_url")
            )


            if not source_url or not source_domain or not target_url:
                continue



            graph["connections"]["verified_backlinks"].append(
                {

                    "source_domain":
                        source_domain,

                    "source_url":
                        source_url,

                    "target_url":
                        target_url,

                    "follow":
                        backlink.get(
                            "follow",
                            False
                        ),

                    "verified":
                        True

                }
            )


            domains.add(
                source_domain
            )



        graph["validation"]["verified_backlinks"] = len(
            graph["connections"]["verified_backlinks"]
        )


        graph["validation"]["backlink_domains"] = len(
            domains
        )


        self.save(
            self.output_file,
            graph
        )


        print(
            "AUTHORITY SOURCE GRAPH CREATED V3"
        )

        print(
            "product_to_source :",
            len(graph["connections"]["product_to_source"])
        )

        print(
            "entity_to_source :",
            len(graph["connections"]["entity_to_source"])
        )

        print(
            "article_to_source :",
            len(graph["connections"]["article_to_source"])
        )

        print(
            "partner_to_source :",
            len(graph["connections"]["partner_to_source"])
        )

        print(
            "verified_backlinks :",
            graph["validation"]["verified_backlinks"]
        )

        print(
            "BACKLINKS CHECKED:",
            graph["validation"]["backlinks_checked"]
        )

        print(
            "BACKLINK DOMAINS:",
            graph["validation"]["backlink_domains"]
        )

        return graph



if __name__ == "__main__":

    AuthoritySourceGraphBuilder().build()
