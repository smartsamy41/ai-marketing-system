import json
from pathlib import Path


class WebExperienceIntelligenceBuilder:


    def __init__(self):

        self.output = Path(
            "data_master/content_intelligence/web_experience_intelligence_graph.json"
        )


    def build(self):

        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "web_experience_intelligence_graph",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "principles":
            {

                "mobile_first":
                True,

                "responsive":
                True,

                "browser_compatible":
                True,

                "accessibility_ready":
                True,

                "legal_ready":
                True,

                "semantic_html":
                True,

                "ai_ready":
                True

            },


            "devices":
            {

                "desktop":
                True,

                "tablet":
                True,

                "mobile":
                True,

                "smartwatch":
                True

            },


            "browsers":
            [

                "Chrome",
                "Edge",
                "Firefox",
                "Safari",
                "Mobile Safari",
                "Android Browser"

            ],


            "html_structure":
            {

                "header":
                [

                    "logo",
                    "navigation",
                    "breadcrumb"

                ],


                "main":
                [

                    "entity_intro",
                    "facts",
                    "content",
                    "questions",
                    "faq",
                    "sources",
                    "affiliate_area"

                ],


                "footer":
                [

                    "category_navigation",
                    "partner_navigation",
                    "legal_links",
                    "affiliate_notice",
                    "social_entities"

                ]

            },


            "accessibility":
            {

                "alt_text_required":
                True,

                "aria_support":
                True,

                "keyboard_navigation":
                True,

                "screen_reader":
                True

            },


            "legal":
            {

                "affiliate_disclosure":
                True,

                "advertising_label":
                True,

                "privacy_required":
                True,

                "imprint_required":
                True

            },


            "seo_ai_layer":
            {

                "schema_org":
                True,

                "json_ld":
                True,

                "open_graph":
                True,

                "canonical":
                True,

                "llms_txt":
                True,

                "entity_connection":
                True

            }

        }


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
            "WEB EXPERIENCE INTELLIGENCE GRAPH CREATED"
        )



if __name__ == "__main__":

    WebExperienceIntelligenceBuilder().build()
