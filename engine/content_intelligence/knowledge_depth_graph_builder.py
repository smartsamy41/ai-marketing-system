import json
from pathlib import Path


class KnowledgeDepthGraphBuilder:


    def __init__(self):

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )

        self.product_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.semantic_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.source_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/knowledge_depth_graph.json"
        )


    def load(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)


    def add_unique(self, target, item):

        if item not in target:
            target.append(item)


    def build(self):

        entities = self.load(self.entity_file)
        products = self.load(self.product_file)
        semantic = self.load(self.semantic_file)
        questions = self.load(self.question_file)
        articles = self.load(self.article_file)
        sources = self.load(self.source_file)


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "knowledge_depth_graph",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "rules":
            {
                "verified_relationships_only": True,
                "source_based": True,
                "no_fake_connections": True
            },

            "depth":
            {
                "entities": [],
                "products": [],
                "topics": [],
                "questions": [],
                "articles": [],
                "sources": []
            },

            "relationships":
            {
                "entity_to_product": [],
                "product_to_topic": [],
                "product_to_question": [],
                "product_to_article": [],
                "article_to_source": []
            }
        }



        # ENTITIES

        for node in entities.get("nodes", {}):

            graph["depth"]["entities"].append(node)



        # PRODUCTS

        for product in products.get(
            "entities",
            []
        ):

            pid = product.get("product_id")

            if pid:

                graph["depth"]["products"].append({

                    "product_id": pid,

                    "entity":
                        product.get("name"),

                    "category":
                        product.get("category"),

                    "partner":
                        product.get("partner")
                })



        # ENTITY -> PRODUCT

        for product in products.get(
            "entities",
            []
        ):

            if product.get("product_id"):

                graph["relationships"]["entity_to_product"].append({

                    "entity":
                        product.get("name"),

                    "product_id":
                        product.get("product_id")

                })



        # TOPICS

        for cluster in semantic.get(
            "clusters",
            []
        ):

            graph["depth"]["topics"].append({

                "topic":
                    cluster.get("cluster"),

                "products":
                    cluster.get("products", [])

            })



        # PRODUCT -> TOPIC

        for item in semantic.get(
            "connections",
            {}
        ).get(
            "topic_to_product",
            []
        ):

            graph["relationships"]["product_to_topic"].append({

                "product_id":
                    item.get("product_id"),

                "topic":
                    item.get("topic")

            })



        # QUESTIONS

        for question in questions.get(
            "questions",
            []
        ):

            graph["depth"]["questions"].append(question)


            graph["relationships"]["product_to_question"].append({

                "product_id":
                    question.get("product_id"),

                "question_id":
                    question.get("question_id")

            })



        # ARTICLES

        for article in articles.get(
            "articles",
            []
        ):

            graph["depth"]["articles"].append(article)


            graph["relationships"]["product_to_article"].append({

                "product_id":
                    article.get("product_id"),

                "article_id":
                    article.get("article_id")

            })



        # SOURCES

        for source in sources.get(
            "connections",
            {}
        ).get(
            "article_to_source",
            []
        ):

            graph["depth"]["sources"].append(source)


            graph["relationships"]["article_to_source"].append({

                "article_id":
                    source.get("article_id"),

                "source":
                    source.get("source")

            })



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
            "KNOWLEDGE DEPTH GRAPH CREATED"
        )


        for key,value in graph["relationships"].items():

            print(
                key,
                len(value)
            )



if __name__ == "__main__":

    KnowledgeDepthGraphBuilder().build()
