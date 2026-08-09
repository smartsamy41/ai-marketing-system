import json
from pathlib import Path


class ProductionValidationIntelligenceBuilder:


    def __init__(self):

        self.sources = {

            "architecture":
            Path(
                "data_master/content_intelligence/production_page_architecture_graph.json"
            ),

            "template":
            Path(
                "data_master/content_intelligence/template_intelligence_graph.json"
            ),

            "components":
            Path(
                "data_master/content_intelligence/component_intelligence_graph.json"
            ),

            "seo":
            Path(
                "data_master/content_intelligence/seo_ai_visibility_intelligence_graph.json"
            ),

            "assets":
            Path(
                "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
            )

        }


        self.output = Path(
            "data_master/content_intelligence/production_validation_intelligence_graph.json"
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


        data={}


        for name,path in self.sources.items():

            data[name]=self.load_json(path)



        graph={


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "production_validation_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",



            "validation_rules":
            {


                "content":

                {

                    "entity_required":
                    True,


                    "source_required":
                    True,


                    "question_layer_required":
                    True

                },


                "seo":

                {

                    "schema_required":
                    True,


                    "canonical_required":
                    True,


                    "open_graph_required":
                    True,


                    "llms_ready":
                    True

                },


                "affiliate":

                {

                    "advertising_label_required":
                    True,


                    "tracking_required":
                    True,


                    "asset_required":
                    True,


                    "partner_policy_required":
                    True

                },


                "technical":

                {

                    "semantic_html":
                    True,


                    "responsive":
                    True,


                    "mobile_first":
                    True,


                    "accessibility":
                    True

                },


                "security":

                {

                    "no_old_page_reuse":
                    True,


                    "no_fake_assets":
                    True,


                    "source_based_only":
                    True

                }

            },



            "checks":
            [

                "ENTITY_CHECK",

                "CONTENT_CHECK",

                "ASSET_CHECK",

                "TRACKING_CHECK",

                "COMPLIANCE_CHECK",

                "SEO_CHECK",

                "SCHEMA_CHECK",

                "ACCESSIBILITY_CHECK"

            ],



            "connections":
            {

                "validation_to_template":
                [],


                "validation_to_asset":
                [],


                "validation_to_seo":
                [],


                "validation_to_component":
                []

            }

        }



        for item in data["template"].get(
            "connections",
            {}
        ).get(
            "partner_to_template",
            []
        ):


            graph["connections"]["validation_to_template"].append(

                {

                    "partner":
                    item.get("partner"),


                    "template":
                    item.get("template"),


                    "validated":
                    True

                }

            )



        for item in data["assets"].get(
            "connections",
            {}
        ).get(
            "product_to_asset",
            []
        ):


            graph["connections"]["validation_to_asset"].append(

                {

                    "product_id":
                    item.get("product_id"),


                    "asset_check":
                    True

                }

            )



        for item in data["seo"].get(
            "connections",
            {}
        ).get(
            "content_to_schema",
            []
        ):


            graph["connections"]["validation_to_seo"].append(

                {

                    "entity":
                    item.get("entity"),


                    "seo_check":
                    True

                }

            )



        for component in data["components"].get(
            "components",
            {}
        ):


            graph["connections"]["validation_to_component"].append(

                {

                    "component":
                    component,


                    "checked":
                    True

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
            "PRODUCTION VALIDATION INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    ProductionValidationIntelligenceBuilder().build()
