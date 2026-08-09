import json
from pathlib import Path


class SEOAIVisibilityIntelligenceBuilder:


    def __init__(self):

        self.content_graph = Path(
            "data_master/content_intelligence/content_experience_intelligence_graph.json"
        )

        self.output = Path(
            "data_master/content_intelligence/seo_ai_visibility_intelligence_graph.json"
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


        content = self.load_json(
            self.content_graph
        )


        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "seo_ai_visibility_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "seo_layer":
            {

                "canonical":
                True,


                "robots":
                True,


                "sitemap":
                True,


                "internal_linking":
                True,


                "semantic_html":
                True

            },


            "schema_layer":
            {

                "json_ld":
                True,


                "schema_types":
                [

                    "Organization",

                    "WebSite",

                    "Article",

                    "FAQPage",

                    "Product",

                    "BreadcrumbList"

                ]

            },


            "ai_layer":
            {

                "llms_txt":
                True,


                "entity_connection":
                True,


                "knowledge_graph":
                True,


                "source_connection":
                True,


                "fact_based_content":
                True

            },


            "open_graph":
            {

                "enabled":
                True,


                "title":
                True,


                "description":
                True,


                "image":
                True,


                "url":
                True

            },


            "connections":
            {

                "content_to_schema":
                [],


                "content_to_entity":
                [],


                "content_to_internal_links":
                [],


                "content_to_ai_layer":
                []

            }

        }



        # bestehende Content Verbindungen übernehmen


        connections = content.get(
            "connections",
            {}
        )


        for item in connections.get(
            "content_to_schema",
            []
        ):


            graph["connections"]["content_to_schema"].append(

                {

                    "entity":
                    item.get("entity"),


                    "schema_ready":
                    True

                }

            )



        for item in connections.get(
            "content_to_entity",
            []
        ):


            graph["connections"]["content_to_entity"].append(

                {

                    "article_id":
                    item.get("article_id"),


                    "entity":
                    item.get("entity")

                }

            )



        for item in connections.get(
            "article_to_question",
            []
        ):


            graph["connections"]["content_to_internal_links"].append(

                {

                    "product_id":
                    item.get("product_id"),


                    "question_id":
                    item.get("question_id")

                }

            )



        for item in graph["connections"]["content_to_entity"]:


            graph["connections"]["content_to_ai_layer"].append(

                {

                    "entity":
                    item.get("entity"),


                    "signals":
                    [

                        "entity",

                        "schema",

                        "knowledge_graph",

                        "llms"

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
            "SEO AI VISIBILITY INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    SEOAIVisibilityIntelligenceBuilder().build()
