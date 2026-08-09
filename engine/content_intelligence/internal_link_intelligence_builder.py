import json
from pathlib import Path


class InternalLinkIntelligenceBuilder:


    def __init__(self):

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.cluster_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.knowledge_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/internal_link_graph.json"
        )



    def load(self,path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):


        articles = self.load(
            self.article_file
        )

        clusters = self.load(
            self.cluster_file
        )

        questions = self.load(
            self.question_file
        )

        knowledge = self.load(
            self.knowledge_file
        )



        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "internal_link_intelligence_graph",

            "version":
                "1.0",

            "status":
                "ACTIVE",


            "connections":
            {

                "article_to_article": [],

                "article_to_topic": [],

                "article_to_product": [],

                "article_to_question": [],

                "article_to_landingpage": []

            }

        }



        article_list = articles.get(
            "articles",
            []
        )


        question_list = questions.get(
            "questions",
            []
        )



        product_topics = {}

        for item in clusters.get(
            "connections",
            {}
        ).get(
            "topic_to_product",
            []
        ):

            product_topics[
                item["product_id"]
            ] = item["topic"]




        landingpages = {}

        for product in knowledge.get(
            "products",
            []
        ):

            pid = product.get(
                "product_id"
            )

            lp = product.get(
                "catalog",
                {}
            ).get(
                "landingpage",
                ""
            )

            if pid and lp:

                landingpages[pid] = lp




        for article in article_list:


            article_id = article.get(
                "article_id"
            )

            product_id = article.get(
                "product_id"
            )


            if article_id and product_id:


                graph["connections"]["article_to_product"].append(

                    {
                        "article_id": article_id,
                        "product_id": product_id
                    }

                )



                if product_id in product_topics:


                    graph["connections"]["article_to_topic"].append(

                        {
                            "article_id": article_id,
                            "topic": product_topics[product_id]
                        }

                    )



                if product_id in landingpages:


                    graph["connections"]["article_to_landingpage"].append(

                        {
                            "article_id": article_id,
                            "landingpage": landingpages[product_id]
                        }

                    )





        for question in question_list:


            product_id = question.get(
                "product_id"
            )


            for article in article_list:


                if article.get(
                    "product_id"
                ) == product_id:


                    graph["connections"]["article_to_question"].append(

                        {
                            "article_id":
                                article.get("article_id"),

                            "question_id":
                                question.get("question_id")

                        }

                    )





        for source in article_list:


            for target in article_list:


                if source.get("article_id") == target.get("article_id"):

                    continue


                if source.get("product_id") == target.get("product_id"):


                    score = 3


                elif product_topics.get(
                    source.get("product_id")
                ) == product_topics.get(
                    target.get("product_id")
                ):


                    score = 2


                else:

                    continue



                graph["connections"]["article_to_article"].append(

                    {

                        "from_article":
                            source.get("article_id"),

                        "to_article":
                            target.get("article_id"),

                        "score":
                            score

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
            "INTERNAL LINK INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    InternalLinkIntelligenceBuilder().build()
