import json
from pathlib import Path
from datetime import datetime, timezone


class EntityTopicBuilder:

    def __init__(self):

        self.entities_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.category_file = Path(
            "data_master/linking/category_map.json"
        )

        self.silo_file = Path(
            "data_master/linking/silo_structure.json"
        )

        self.cluster_file = Path(
            "data_master/content_intelligence/topic_cluster_registry.json"
        )

        self.output_file = Path(
            "data_master/content_graph/entity_topic_graph.json"
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
            self.entities_file
        )

        categories = self.load(
            self.category_file
        ).get(
            "categories",
            {}
        )

        silos = self.load(
            self.silo_file
        ).get(
            "silos",
            {}
        )

        clusters = self.load(
            self.cluster_file
        ).get(
            "clusters",
            []
        )


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "entity_topic_graph",

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
                    "entity_based": True,
                    "no_fake_relationships": True
                },

            "entities": [],

            "topics": [],

            "relationships":
                {
                    "entity_to_topic": [],
                    "topic_to_cluster": [],
                    "topic_to_product": [],
                    "topic_to_article": [],
                    "topic_to_question": []
                }
        }


        topics=set()


        for entity in entities.get(
            "entities",
            []
        ):

            product_id = entity.get(
                "product_id"
            )

            category = entity.get(
                "category",
                ""
            ).lower()


            topic = ""


            for key,value in categories.items():

                if product_id == value.get(
                    "product_id"
                ):

                    topic=value.get(
                        "silo",
                        ""
                    )



                if product_id in value.get(
                    "product_ids",
                    []
                ):

                    topic=value.get(
                        "silo",
                        ""
                    )


            if not topic:

                topic=category



            topics.add(topic)



            graph["entities"].append(
                entity
            )


            graph["relationships"]["entity_to_topic"].append(

                {
                    "entity":
                        product_id,

                    "topic":
                        topic
                }

            )


            graph["relationships"]["topic_to_product"].append(

                {
                    "topic":
                        topic,

                    "product_id":
                        product_id
                }

            )


        for cluster in clusters:

            topic = cluster.get(
                "cluster"
            )

            graph["relationships"]["topic_to_cluster"].append(

                {
                    "topic":
                        topic,

                    "product_id":
                        cluster.get(
                            "product_id"
                        ),

                    "category":
                        cluster.get(
                            "category"
                        )

                }

            )

            topics.add(topic)



        graph["topics"] = sorted(
            list(topics)
        )


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
                graph,
                f,
                indent=2,
                ensure_ascii=False
            )


        return graph



if __name__ == "__main__":

    builder = EntityTopicBuilder()

    result = builder.build()

    print(
        "ENTITY TOPIC GRAPH CREATED"
    )

    print(
        "Entities:",
        len(result["entities"])
    )

    print(
        "Topics:",
        len(result["topics"])
    )
