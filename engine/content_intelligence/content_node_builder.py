import json
from pathlib import Path
from datetime import datetime, timezone


class ContentNodeBuilder:

    def __init__(self):

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.topic_file = Path(
            "data_master/content_graph/entity_topic_graph.json"
        )

        self.relationship_file = Path(
            "data_master/content_graph/content_relationships.json"
        )

        self.output_file = Path(
            "data_master/content_graph/content_nodes.json"
        )


    def load(self, file):

        if not file.exists():
            return {}

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)



    def build(self):

        entities = self.load(
            self.entity_file
        )

        topics = self.load(
            self.topic_file
        )

        relationships = self.load(
            self.relationship_file
        )


        nodes = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "content_graph_nodes",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "rules":
                {
                    "source_required": True,
                    "entity_required": True,
                    "no_orphan_content": True,
                    "verified_content_only": True
                },


            "nodes":
                {

                    "products": [],

                    "partners": [],

                    "categories": [],

                    "topics": [],

                    "questions": [],

                    "articles": [],

                    "landingpages": [],

                    "faq": [],

                    "locations": [],

                    "newsletters": [],

                    "sources": []

                }

        }



        #
        # PRODUCTS
        #

        for entity in entities.get(
            "entities",
            []
        ):

            nodes["nodes"]["products"].append(

                {
                    "product_id":
                        entity.get("product_id"),

                    "name":
                        entity.get("name"),

                    "partner":
                        entity.get("partner"),

                    "category":
                        entity.get("category"),

                    "knowledge_status":
                        entity.get(
                            "knowledge_status",
                            ""
                        )

                }

            )



            partner = entity.get(
                "partner"
            )

            if partner and partner not in nodes["nodes"]["partners"]:

                nodes["nodes"]["partners"].append(
                    partner
                )


            category = entity.get(
                "category"
            )

            if category and category not in nodes["nodes"]["categories"]:

                nodes["nodes"]["categories"].append(
                    category
                )



        #
        # TOPICS
        #

        for topic in topics.get(
            "topics",
            []
        ):

            nodes["nodes"]["topics"].append(
                {
                    "topic":
                        topic
                }
            )



        #
        # ARTICLES + LANDINGPAGES
        #

        for item in relationships.get(
            "relationships",
            {}
        ).get(
            "product_to_article",
            []
        ):

            nodes["nodes"]["articles"].append(

                {
                    "product_id":
                        item.get("product_id"),

                    "article":
                        item.get("article")

                }

            )



        for item in relationships.get(
            "relationships",
            {}
        ).get(
            "product_to_landingpage",
            []
        ):

            nodes["nodes"]["landingpages"].append(

                {
                    "product_id":
                        item.get("product_id"),

                    "landingpage":
                        item.get("landingpage")

                }

            )



        #
        # SOURCES vorbereiten
        #

        for entity in entities.get(
            "entities",
            []
        ):

            for source in entity.get(
                "source",
                []
            ):

                nodes["nodes"]["sources"].append(
                    {
                        "product_id":
                            entity.get("product_id"),

                        "source":
                            source
                    }
                )



        #
        # speichern
        #

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                nodes,
                f,
                indent=2,
                ensure_ascii=False
            )


        return nodes



if __name__ == "__main__":

    builder = ContentNodeBuilder()

    result = builder.build()


    print(
        "CONTENT NODE GRAPH CREATED"
    )


    for key,value in result["nodes"].items():

        print(
            key,
            ":",
            len(value)
        )
