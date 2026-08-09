import json
from pathlib import Path


class ContentExperienceIntelligenceBuilder:


    def __init__(self):

        self.sources = {

            "articles":
            Path(
                "data_master/content_graph/article_intelligence_graph.json"
            ),

            "questions":
            Path(
                "data_master/content_intelligence/question_intelligence_graph.json"
            ),

            "knowledge":
            Path(
                "data_master/content_intelligence/knowledge_depth_graph.json"
            ),

            "navigation":
            Path(
                "data_master/content_intelligence/navigation_intelligence_graph.json"
            ),

            "assets":
            Path(
                "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
            ),

            "selection":
            Path(
                "data_master/content_intelligence/asset_selection_intelligence_graph.json"
            )

        }


        self.output = Path(
            "data_master/content_intelligence/content_experience_intelligence_graph.json"
        )



    def load_json(self,path):

        if not path.exists():

            return {}


        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):


        loaded={}


        for name,path in self.sources.items():

            loaded[name]=self.load_json(
                path
            )



        graph={


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "content_experience_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "principles":
            {

                "semantic_html":
                True,

                "mobile_first":
                True,

                "responsive":
                True,

                "accessibility":
                True,

                "ai_ready":
                True,

                "schema_ready":
                True,

                "entity_connected":
                True

            },


            "page_structure":
            {

                "header":

                [

                    "entity",

                    "title",

                    "direct_answer"

                ],


                "main_content":

                [

                    "article",

                    "facts",

                    "questions",

                    "faq",

                    "sources"

                ],


                "conversion_area":

                [

                    "selected_asset",

                    "partner_notice",

                    "tracking"

                ],


                "related_area":

                [

                    "related_articles",

                    "related_questions",

                    "related_products"

                ],


                "footer":

                [

                    "partner_information",

                    "legal_information",

                    "disclosure"

                ]

            },


            "connections":
            {

                "article_to_question":

                [],


                "article_to_asset":

                [],


                "article_to_navigation":

                [],


                "product_to_experience":

                [],


                "content_to_schema":

                [],


                "content_to_entity":

                []

            }

        }



        # Artikel verbinden

        article_graph = loaded["articles"]


        for item in article_graph.get(
            "articles",
            []
        ):


            article_id=item.get(
                "article_id"
            )


            product_id=item.get(
                "product_id"
            )


            graph["connections"]["product_to_experience"].append(

                {

                    "product_id":
                    product_id,


                    "article_id":
                    article_id,


                    "experience":
                    "FULL_CONTENT_PAGE"

                }

            )



            graph["connections"]["content_to_entity"].append(

                {

                    "article_id":
                    article_id,


                    "entity":
                    item.get("entity")

                }

            )



        # Fragen verbinden

        question_graph = loaded["questions"]


        for q in question_graph.get(
            "questions",
            []
        ):


            graph["connections"]["article_to_question"].append(

                {

                    "product_id":
                    q.get("product_id"),


                    "question_id":
                    q.get("question_id")

                }

            )



        # Assets verbinden

        asset_graph=loaded["assets"]


        for asset in asset_graph.get(
            "assets",
            []
        ):


            graph["connections"]["article_to_asset"].append(

                {

                    "asset_id":
                    asset.get("asset_id"),


                    "usage":
                    "AUTO_SELECTED"

                }

            )



        # Navigation

        nav_graph=loaded["navigation"]


        for key,value in nav_graph.get(
            "connections",
            {}
        ).items():


            graph["connections"]["article_to_navigation"].append(

                {

                    "type":
                    key,


                    "count":
                    len(value)

                }

            )



        # Schema Layer

        for item in graph["connections"]["content_to_entity"]:

            graph["connections"]["content_to_schema"].append(

                {

                    "entity":
                    item["entity"],


                    "schema":

                    [

                        "Article",

                        "FAQPage",

                        "Organization",

                        "Product"

                    ]

                }

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
            "CONTENT EXPERIENCE INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__=="__main__":

    ContentExperienceIntelligenceBuilder().build()
