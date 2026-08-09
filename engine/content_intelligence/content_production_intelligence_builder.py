import json
from pathlib import Path


class ContentProductionIntelligenceBuilder:


    def __init__(self):

        self.entity_graph = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )

        self.content_graph = Path(
            "data_master/content_graph/content_relationships.json"
        )

        self.question_graph = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.authority_graph = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )

        self.output = Path(
            "data_master/content_intelligence/content_production_intelligence_graph.json"
        )



    def load(self, path):

        if not path.exists():

            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):


        entity = self.load(
            self.entity_graph
        )

        content = self.load(
            self.content_graph
        )

        questions = self.load(
            self.question_graph
        )

        authority = self.load(
            self.authority_graph
        )



        graph = {


            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "content_production_intelligence_graph",


            "version":
                "1.0",


            "status":
                "ACTIVE",


            "rules":
            {

                "entity_connected":
                    True,

                "source_based":
                    True,

                "compliance_required":
                    True,

                "semantic_html":
                    True,

                "ai_ready":
                    True

            },


            "html_architecture":
            {

                "head":
                [

                    "title",
                    "meta_description",
                    "canonical",
                    "open_graph",
                    "twitter_card",
                    "json_ld",
                    "schema_org"

                ],


                "body":
                [

                    "entity_intro",
                    "facts",
                    "content",
                    "questions",
                    "faq",
                    "affiliate_area",
                    "sources",
                    "internal_links"

                ],


                "footer":
                [

                    "category_navigation",
                    "partner_navigation",
                    "about_freebasics",
                    "affiliate_notice",
                    "privacy",
                    "imprint",
                    "sitemap"

                ]

            },


            "connections":
            {

                "entity_to_content": [],

                "product_to_question": [],

                "product_to_article": [],

                "article_to_source": [],

                "product_to_navigation": []

            }

        }



        for product in entity.get(
            "nodes",
            {}
        ).get(
            "products",
            []
        ):

            graph["connections"]["entity_to_content"].append(

                {

                    "entity":
                        product.get("id"),

                    "content_type":
                        "product_knowledge_node"

                }

            )



        for relation in content.get(
            "relationships",
            []
        ):

            graph["connections"]["product_to_article"].append(
                relation
            )



        for item in questions.get(
            "connections",
            {}
        ).get(
            "question_to_product",
            []
        ):

            graph["connections"]["product_to_question"].append(
                item
            )



        for item in authority.get(
            "connections",
            {}
        ).get(
            "article_to_source",
            []
        ):

            graph["connections"]["article_to_source"].append(
                item
            )



        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output,
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
            "CONTENT PRODUCTION INTELLIGENCE GRAPH CREATED"
        )


        for key,value in graph["connections"].items():

            print(
                key,
                ":",
                len(value)
            )





if __name__ == "__main__":

    ContentProductionIntelligenceBuilder().build()
