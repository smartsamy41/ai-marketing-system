import json
from pathlib import Path


class TemplateIntelligenceBuilder:


    def __init__(self):

        self.sources = {

            "partner_policy":
            Path(
                "data_master/content_intelligence/partner_policy_intelligence.json"
            ),

            "components":
            Path(
                "data_master/content_intelligence/component_intelligence_graph.json"
            ),

            "experience":
            Path(
                "data_master/content_intelligence/content_experience_intelligence_graph.json"
            )

        }


        self.output = Path(
            "data_master/content_intelligence/template_intelligence_graph.json"
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
            "template_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",



            "templates":
            {


                "affiliate_comparison":

                {

                    "partners":

                    [

                        "check24",

                        "tarifcheck"

                    ],


                    "sections":

                    [

                        "entity",

                        "direct_answer",

                        "facts",

                        "comparison_area",

                        "affiliate_asset",

                        "faq",

                        "sources",

                        "footer"

                    ],


                    "conversion":

                    "affiliate"

                },



                "product_guide":

                {

                    "partners":

                    [

                        "amazon"

                    ],


                    "sections":

                    [

                        "entity",

                        "product_information",

                        "original_image",

                        "facts",

                        "faq",

                        "related_products",

                        "affiliate_link"

                    ],


                    "conversion":

                    "affiliate_product"

                },



                "knowledge_article":

                {

                    "partners":

                    [

                        "telekom"

                    ],


                    "sections":

                    [

                        "entity",

                        "topic",

                        "article",

                        "questions",

                        "faq",

                        "sources",

                        "related_content"

                    ],


                    "conversion":

                    "official_shop_redirect"

                }

            },



            "rules":

            {

                "no_old_landingpage_reuse":

                True,


                "source_based_content_only":

                True,


                "partner_policy_required":

                True,


                "asset_selection_required":

                True

            },



            "connections":

            {

                "partner_to_template":

                [],


                "template_to_component":

                [],


                "template_to_conversion":

                []

            }

        }



        policies=data["partner_policy"].get(
            "partners",
            {}
        )


        for partner,rules in policies.items():


            if partner in [

                "check24",

                "tarifcheck"

            ]:


                template="affiliate_comparison"


            elif partner=="amazon":


                template="product_guide"


            elif partner=="telekom":


                template="knowledge_article"


            else:


                continue



            graph["connections"]["partner_to_template"].append(

                {

                    "partner":
                    partner,


                    "template":
                    template

                }

            )



            graph["connections"]["template_to_conversion"].append(

                {

                    "template":
                    template,


                    "conversion":
                    graph["templates"][template]["conversion"]

                }

            )



        for template,config in graph["templates"].items():


            for section in config["sections"]:

                graph["connections"]["template_to_component"].append(

                    {

                        "template":
                        template,


                        "component":
                        section

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
            "TEMPLATE INTELLIGENCE GRAPH CREATED"
        )


        print(
            "TEMPLATES:",
            len(graph["templates"])
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__=="__main__":

    TemplateIntelligenceBuilder().build()
