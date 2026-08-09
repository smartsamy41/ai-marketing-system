import json
from pathlib import Path


class ArticleGraphBuilder:


    def __init__(self):

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.topic_file = Path(
            "data_master/content_intelligence/topic_cluster_registry.json"
        )

        self.knowledge_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.source_file = Path(
            "data_master/source_layer/primary_sources.json"
        )

        self.output_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
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

        entities = self.load(
            self.entity_file
        )

        topics = self.load(
            self.topic_file
        )

        knowledge = self.load(
            self.knowledge_file
        )

        sources = self.load(
            self.source_file
        )


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "article_intelligence_graph",

            "version":
                "1.0",

            "status":
                "ACTIVE",


            "rules":
            {
                "entity_required": True,
                "topic_required": True,
                "landingpage_connection_required": True,
                "source_validation_required": True,
                "no_fake_relationships": True
            },


            "articles": [],


            "connections":
            {

                "article_to_entity": [],

                "article_to_topic": [],

                "article_to_product": [],

                "article_to_landingpage": [],

                "article_to_source": []

            }

        }



        products = entities.get(
            "entities",
            []
        )


        clusters = topics.get(
            "clusters",
            []
        )



        landingpages = {}

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

                landingpages[product_id] = landingpage




        for product in products:


            product_id = product.get(
                "product_id",
                ""
            )


            if not product_id:

                continue



            article_id = (
                "ARTICLE_"
                +
                product_id
            )



            graph["articles"].append(

                {

                    "article_id":
                        article_id,

                    "product_id":
                        product_id,

                    "entity":
                        product.get(
                            "name",
                            ""
                        ),

                    "category":
                        product.get(
                            "category",
                            ""
                        ),

                    "partner":
                        product.get(
                            "partner",
                            ""
                        ),

                    "status":
                        "CONNECTED"

                }

            )



            graph["connections"]["article_to_entity"].append(

                {

                    "article_id":
                        article_id,

                    "entity_id":
                        product_id

                }

            )



            graph["connections"]["article_to_product"].append(

                {

                    "article_id":
                        article_id,

                    "product_id":
                        product_id

                }

            )



            if product_id in landingpages:


                graph["connections"]["article_to_landingpage"].append(

                    {

                        "article_id":
                            article_id,

                        "product_id":
                            product_id,

                        "landingpage":
                            landingpages[product_id]

                    }

                )



            for cluster in clusters:


                if cluster.get(
                    "product_id"
                ) == product_id:


                    graph["connections"]["article_to_topic"].append(

                        {

                            "article_id":
                                article_id,

                            "topic":
                                cluster.get(
                                    "cluster"
                                )

                        }

                    )



            source = product.get(
                "source",
                ""
            )


            if source:


                graph["connections"]["article_to_source"].append(

                    {

                        "article_id":
                            article_id,

                        "source":
                            source

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
            "ARTICLE INTELLIGENCE GRAPH CREATED"
        )


        for key,value in graph["connections"].items():

            print(
                key,
                ":",
                len(value)
            )


        return graph





if __name__ == "__main__":


    builder = ArticleGraphBuilder()

    builder.build()
