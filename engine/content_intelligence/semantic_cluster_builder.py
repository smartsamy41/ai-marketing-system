import json
from pathlib import Path


class SemanticClusterBuilder:


    def __init__(self):

        self.topic_file = Path(
            "data_master/content_intelligence/topic_cluster_registry.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.knowledge_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
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



    def build(self):


        topics = self.load(
            self.topic_file
        )


        questions = self.load(
            self.question_file
        )


        articles = self.load(
            self.article_file
        )


        knowledge = self.load(
            self.knowledge_file
        )



        graph = {


            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "semantic_cluster_graph",


            "version":
                "1.0",


            "status":
                "ACTIVE",



            "rules":
            {

                "verified_topics_only":
                    True,

                "product_connection_required":
                    True,

                "landingpage_connection_required":
                    True,

                "no_fake_clusters":
                    True

            },



            "clusters": [],



            "connections":
            {

                "topic_to_product": [],

                "cluster_to_question": [],

                "cluster_to_article": [],

                "cluster_to_landingpage": []

            }

        }



        product_landingpages = {}



        for product in knowledge.get(
            "products",
            []
        ):


            product_id = product.get(
                "product_id",
                ""
            )


            landingpage = product.get(
                "catalog",
                {}
            ).get(
                "landingpage",
                ""
            )


            if product_id and landingpage:

                product_landingpages[product_id] = landingpage





        cluster_map = {}



        for item in topics.get(
            "clusters",
            []
        ):


            cluster = item.get(
                "cluster",
                ""
            )


            product_id = item.get(
                "product_id",
                ""
            )


            category = item.get(
                "category",
                ""
            )



            if not cluster:

                continue



            if cluster not in cluster_map:


                cluster_map[cluster] = {


                    "cluster":
                        cluster,


                    "categories":
                        [],


                    "products":
                        [],


                    "landingpages":
                        []

                }



            if category not in cluster_map[cluster]["categories"]:


                cluster_map[cluster]["categories"].append(
                    category
                )



            if product_id not in cluster_map[cluster]["products"]:


                cluster_map[cluster]["products"].append(
                    product_id
                )



            if product_id in product_landingpages:


                if product_landingpages[product_id] not in cluster_map[cluster]["landingpages"]:


                    cluster_map[cluster]["landingpages"].append(
                        product_landingpages[product_id]
                    )



            graph["connections"]["topic_to_product"].append(

                {

                    "topic":
                        cluster,

                    "product_id":
                        product_id

                }

            )





        for cluster in cluster_map.values():

            graph["clusters"].append(
                cluster
            )





        for question in questions.get(
            "questions",
            []
        ):


            product_id = question.get(
                "product_id",
                ""
            )



            for cluster in graph["clusters"]:


                if product_id in cluster["products"]:


                    graph["connections"]["cluster_to_question"].append(

                        {

                            "cluster":
                                cluster["cluster"],

                            "question_id":
                                question.get(
                                    "question_id"
                                )

                        }

                    )





        for article in articles.get(
            "articles",
            []
        ):


            product_id = article.get(
                "product_id",
                ""
            )



            for cluster in graph["clusters"]:


                if product_id in cluster["products"]:


                    graph["connections"]["cluster_to_article"].append(

                        {

                            "cluster":
                                cluster["cluster"],

                            "article_id":
                                article.get(
                                    "article_id"
                                )

                        }

                    )





        for cluster in graph["clusters"]:


            for landingpage in cluster.get(
                "landingpages",
                []
            ):


                graph["connections"]["cluster_to_landingpage"].append(

                    {

                        "cluster":
                            cluster["cluster"],

                        "landingpage":
                            landingpage

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
            "SEMANTIC CLUSTER GRAPH CREATED"
        )


        print(
            "CLUSTERS:",
            len(graph["clusters"])
        )



        for key,value in graph["connections"].items():

            print(
                key,
                ":",
                len(value)
            )



        return graph





if __name__ == "__main__":


    builder = SemanticClusterBuilder()

    builder.build()
