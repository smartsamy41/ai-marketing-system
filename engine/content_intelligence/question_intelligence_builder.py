import json
from pathlib import Path


class QuestionIntelligenceBuilder:


    def __init__(self):

        self.topic_file = Path(
            "data_master/content_intelligence/question_graph.json"
        )

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )



    def load(self, path):

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build_question_templates(
        self,
        product
    ):

        name = product.get(
            "name",
            ""
        )

        category = product.get(
            "category",
            ""
        )

        product_id = product.get(
            "product_id",
            ""
        )


        questions = []


        if name:


            questions.append(

                {

                    "question_id":
                        "Q_" + product_id + "_001",

                    "question":
                        f"Was ist {name}?",

                    "intent":
                        "informational",

                    "product_id":
                        product_id,

                    "category":
                        category

                }

            )



            questions.append(

                {

                    "question_id":
                        "Q_" + product_id + "_002",

                    "question":
                        f"Welche Informationen gibt es zu {name}?",

                    "intent":
                        "informational",

                    "product_id":
                        product_id,

                    "category":
                        category

                }

            )



            questions.append(

                {

                    "question_id":
                        "Q_" + product_id + "_003",

                    "question":
                        f"Wie kann ich {name} prüfen?",

                    "intent":
                        "commercial",

                    "product_id":
                        product_id,

                    "category":
                        category

                }

            )


        return questions



    def build(self):


        entities = self.load(
            self.entity_file
        )


        articles = self.load(
            self.article_file
        )


        topic_graph = self.load(
            self.topic_file
        )



        graph = {


            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "question_intelligence_graph",


            "version":
                "1.0",


            "status":
                "ACTIVE",


            "rules":
            {

                "source_based":
                    True,

                "entity_required":
                    True,

                "article_connection_required":
                    True,

                "no_fake_questions":
                    True

            },


            "questions": [],


            "connections":
            {

                "question_to_entity": [],

                "question_to_article": [],

                "question_to_topic": [],

                "question_to_product": []

            }


        }



        products = entities.get(
            "entities",
            []
        )



        article_map = {}


        for article in articles.get(
            "articles",
            []
        ):


            article_map[
                article.get(
                    "product_id"
                )
            ] = article.get(
                "article_id"
            )



        for product in products:


            product_id = product.get(
                "product_id",
                ""
            )


            questions = self.build_question_templates(
                product
            )



            for question in questions:


                graph["questions"].append(
                    question
                )


                graph["connections"]["question_to_product"].append(

                    {

                        "question_id":
                            question["question_id"],

                        "product_id":
                            product_id

                    }

                )



                graph["connections"]["question_to_entity"].append(

                    {

                        "question_id":
                            question["question_id"],

                        "entity_id":
                            product_id

                    }

                )



                if product_id in article_map:


                    graph["connections"]["question_to_article"].append(

                        {

                            "question_id":
                                question["question_id"],

                            "article_id":
                                article_map[product_id]

                        }

                    )



        for topic in topic_graph.get(
            "topic_connections",
            []
        ):


            for entity in topic.get(
                "entities",
                []
            ):


                for question in graph["questions"]:


                    if question.get(
                        "product_id"
                    ) == entity:


                        graph["connections"]["question_to_topic"].append(

                            {

                                "question_id":
                                    question["question_id"],

                                "topic":
                                    topic.get(
                                        "topic"
                                    )

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
            "QUESTION INTELLIGENCE GRAPH CREATED"
        )


        print(
            "QUESTIONS:",
            len(graph["questions"])
        )


        for key,value in graph["connections"].items():

            print(
                key,
                ":",
                len(value)
            )



        return graph





if __name__ == "__main__":


    builder = QuestionIntelligenceBuilder()

    builder.build()
