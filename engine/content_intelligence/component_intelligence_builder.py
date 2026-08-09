import json
from pathlib import Path


class ComponentIntelligenceBuilder:


    def __init__(self):

        self.source = Path(
            "data_master/content_intelligence/production_page_architecture_graph.json"
        )


        self.output = Path(
            "data_master/content_intelligence/component_intelligence_graph.json"
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


        architecture = self.load_json(
            self.source
        )


        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "component_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",



            "components":
            {


                "header":
                {

                    "purpose":
                    "page_identity",

                    "elements":
                    [

                        "entity",

                        "topic",

                        "title",

                        "navigation"

                    ]

                },


                "direct_answer":
                {

                    "purpose":
                    "quick_information",

                    "elements":
                    [

                        "short_answer",

                        "facts"

                    ]

                },


                "content":
                {

                    "purpose":
                    "main_information",

                    "elements":
                    [

                        "introduction",

                        "article",

                        "questions",

                        "faq",

                        "sources"

                    ]

                },


                "affiliate_block":
                {

                    "purpose":
                    "partner_conversion",

                    "elements":
                    [

                        "advertising_label",

                        "selected_asset",

                        "tracking",

                        "partner_notice"

                    ]

                },


                "related_content":
                {

                    "purpose":
                    "content_navigation",

                    "elements":
                    [

                        "related_articles",

                        "related_questions",

                        "related_products"

                    ]

                },


                "footer":
                {

                    "purpose":
                    "legal_information",

                    "elements":
                    [

                        "imprint",

                        "privacy",

                        "cookie",

                        "affiliate_disclosure",

                        "partner_information"

                    ]

                }

            },


            "technical_components":
            {

                "semantic_html":

                [

                    "header",

                    "main",

                    "section",

                    "article",

                    "aside",

                    "footer"

                ],


                "accessibility":

                [

                    "aria",

                    "alt_text",

                    "keyboard_navigation",

                    "screen_reader"

                ],


                "seo":

                [

                    "title",

                    "meta",

                    "canonical",

                    "schema",

                    "open_graph"

                ]


            },


            "connections":
            {

                "component_to_page":

                [],


                "component_to_schema":

                [],


                "component_to_asset":

                [],


                "component_to_compliance":

                []

            }

        }



        # Architektur verbinden


        for item in architecture.get(
            "connections",
            {}
        ).get(
            "page_to_content",
            []
        ):


            graph["connections"]["component_to_page"].append(

                {

                    "product_id":
                    item.get("product_id"),


                    "component":
                    "content_page"

                }

            )



        for item in architecture.get(
            "connections",
            {}
        ).get(
            "page_to_asset",
            []
        ):


            graph["connections"]["component_to_asset"].append(

                {

                    "asset_id":
                    item.get("asset_id"),


                    "component":
                    "affiliate_block"

                }

            )



        for item in architecture.get(
            "connections",
            {}
        ).get(
            "page_to_seo",
            []
        ):


            graph["connections"]["component_to_schema"].append(

                {

                    "entity":
                    item.get("entity"),


                    "schema":
                    True

                }

            )



        graph["connections"]["component_to_compliance"].append(

            {

                "component":
                "affiliate_block",


                "rules":
                [

                    "advertising_label",

                    "tracking",

                    "partner_rules"

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
            "COMPONENT INTELLIGENCE GRAPH CREATED"
        )


        print(
            "COMPONENTS:",
            len(graph["components"])
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    ComponentIntelligenceBuilder().build()
