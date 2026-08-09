import json
from pathlib import Path


class QuestionGraphBuilder:

    def __init__(self):

        self.topic_file = Path(
            "data_master/content_intelligence/topic_cluster_registry.json"
        )

        self.entity_file = Path(
            "data_master/content_graph/entity_topic_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/question_graph.json"
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

        topics = self.load(
            self.topic_file
        )

        entities = self.load(
            self.entity_file
        )


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "question_graph",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules":
            {

                "source_required":
                    True,

                "intent_required":
                    True,

                "no_fake_search_questions":
                    True,

                "entity_connection_required":
                    True

            },


            "intents":
            {

                "informational": [],

                "commercial": [],

                "transactional": [],

                "navigational": []

            },


            "topic_connections":
                [],


            "questions":
                []

        }



        topic_map = {}


        for item in topics.get(
            "clusters",
            []
        ):

            topic = item.get(
                "cluster"
            )


            topic_map.setdefault(
                topic,
                []
            )


            topic_map[topic].append(
                item.get(
                    "product_id"
                )
            )



        for topic, products in topic_map.items():

            graph["topic_connections"].append(

                {

                    "topic":
                        topic,

                    "entities":
                        products

                }

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


        print(
            "QUESTION GRAPH CREATED"
        )


        return graph



if __name__ == "__main__":

    builder = QuestionGraphBuilder()

    builder.build()
