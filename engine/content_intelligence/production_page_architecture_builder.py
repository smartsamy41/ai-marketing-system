import json
from pathlib import Path


class ProductionPageArchitectureBuilder:


    def __init__(self):

        self.sources = {

            "experience":
            Path(
                "data_master/content_intelligence/content_experience_intelligence_graph.json"
            ),

            "seo":
            Path(
                "data_master/content_intelligence/seo_ai_visibility_intelligence_graph.json"
            ),

            "assets":
            Path(
                "data_master/content_intelligence/asset_selection_intelligence_graph.json"
            ),

            "partner_policy":
            Path(
                "data_master/content_intelligence/partner_policy_intelligence.json"
            )

        }


        self.output = Path(
            "data_master/content_intelligence/production_page_architecture_graph.json"
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
            "production_page_architecture",


            "version":
            "1.0",


            "status":
            "ACTIVE",



            "page_structure":
            {


                "head":
                [

                    "title",

                    "meta_description",

                    "canonical",

                    "open_graph",

                    "json_ld"

                ],


                "header":
                [

                    "entity",

                    "topic",

                    "direct_answer"

                ],


                "main":
                [

                    "introduction",

                    "facts",

                    "article_content",

                    "questions",

                    "faq",

                    "sources"

                ],


                "affiliate_area":
                [

                    "advertising_label",

                    "selected_asset",

                    "tracking",

                    "partner_notice"

                ],


                "related":
                [

                    "related_articles",

                    "related_questions",

                    "related_products"

                ],


                "footer":
                [

                    "imprint",

                    "privacy",

                    "cookie",

                    "affiliate_disclosure",

                    "partner_information"

                ]

            },



            "technical_requirements":
            {

                "semantic_html":
                True,

                "responsive":
                True,

                "mobile_first":
                True,

                "browser_compatible":
                True,

                "accessibility_ready":
                True,

                "schema_ready":
                True,

                "ai_ready":
                True

            },



            "connections":
            {

                "page_to_content":
                [],


                "page_to_seo":
                [],


                "page_to_asset":
                [],


                "page_to_partner_policy":
                []

            }

        }



        experience = loaded["experience"]


        for item in experience.get(
            "connections",
            {}
        ).get(
            "product_to_experience",
            []
        ):


            graph["connections"]["page_to_content"].append(

                {

                    "product_id":
                    item.get("product_id"),


                    "article_id":
                    item.get("article_id"),


                    "page_type":
                    "CONTENT_EXPERIENCE_PAGE"

                }

            )



        seo = loaded["seo"]


        for item in seo.get(
            "connections",
            {}
        ).get(
            "content_to_schema",
            []
        ):


            graph["connections"]["page_to_seo"].append(

                {

                    "entity":
                    item.get("entity"),


                    "schema_ready":
                    True

                }

            )



        assets = loaded["assets"]


        for item in assets.get(
            "assets",
            []
        ):


            graph["connections"]["page_to_asset"].append(

                {

                    "asset_id":
                    item.get("asset_id"),


                    "selection":
                    "AUTO"

                }

            )



        policies = loaded["partner_policy"]


        for partner in policies.get(
            "partners",
            {}
        ):


            graph["connections"]["page_to_partner_policy"].append(

                {

                    "partner":
                    partner,


                    "policy":
                    "CONNECTED"

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
            "PRODUCTION PAGE ARCHITECTURE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    ProductionPageArchitectureBuilder().build()
