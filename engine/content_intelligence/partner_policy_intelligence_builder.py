import json
from pathlib import Path


class PartnerPolicyIntelligenceBuilder:


    def __init__(self):

        self.output = Path(
            "data_master/content_intelligence/partner_policy_intelligence.json"
        )


    def build(self):


        data = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "partner_policy_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "partners":
            {


                "check24":
                {

                    "content_layer": True,

                    "article_generation": True,

                    "landingpage": True,

                    "affiliate_conversion": True,

                    "assets": True,

                    "tracking": True

                },


                "tarifcheck":
                {

                    "content_layer": True,

                    "article_generation": True,

                    "landingpage": True,

                    "affiliate_conversion": True,

                    "calculator_widgets": True,

                    "tracking": True,

                    "compliance_required": True

                },


                "amazon":
                {

                    "content_layer": True,

                    "article_generation": True,

                    "product_content": True,

                    "original_images_only": True,

                    "affiliate_link": True,

                    "tracking": True

                },


                "telekom":
                {

                    "content_layer": True,

                    "entity_layer": True,

                    "article_generation": True,

                    "newsletter_content": True,

                    "faq_generation": True,

                    "internal_linking": True,

                    "schema_generation": True,

                    "official_assets_only": True,

                    "conversion_landingpage": False,

                    "external_shop_redirect": True

                }

            },


            "renderer_rules":
            {


                "affiliate_partners":
                [

                    "check24",

                    "tarifcheck",

                    "amazon"

                ],


                "shop_redirect_partners":
                [

                    "telekom"

                ]

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
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


        print(
            "PARTNER POLICY INTELLIGENCE CREATED"
        )



if __name__ == "__main__":

    PartnerPolicyIntelligenceBuilder().build()
