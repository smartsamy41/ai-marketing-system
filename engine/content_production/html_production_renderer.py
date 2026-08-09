import json
from pathlib import Path
from datetime import datetime


class HTMLProductionRenderer:


    def __init__(self):

        self.sources = {

            "architecture":
            Path(
                "data_master/content_intelligence/production_page_architecture_graph.json"
            ),

            "components":
            Path(
                "data_master/content_intelligence/component_intelligence_graph.json"
            ),

            "templates":
            Path(
                "data_master/content_intelligence/template_intelligence_graph.json"
            ),

            "validation":
            Path(
                "data_master/content_intelligence/production_validation_intelligence_graph.json"
            )

        }


        self.output = Path(
            "data_master/content_production/rendered_page_architecture.json"
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



        pages=[]


        architecture=data["architecture"]


        for item in architecture.get(
            "connections",
            {}
        ).get(
            "page_to_content",
            []
        ):


            page={


                "product_id":
                item.get("product_id"),


                "article_id":
                item.get("article_id"),


                "template":
                "AUTO_SELECT",


                "html_structure":
                {


                    "head":
                    [

                        "title",

                        "meta_description",

                        "canonical",

                        "open_graph",

                        "json_ld"

                    ],


                    "body":
                    [

                        "header",

                        "direct_answer",

                        "main_content",

                        "affiliate_area",

                        "related_content",

                        "footer"

                    ]

                },


                "status":
                "READY_FOR_RENDER"

            }


            pages.append(page)



        graph={


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "html_production_renderer",


            "version":
            "1.0",


            "created":
            datetime.utcnow().isoformat(),


            "status":
            "ACTIVE",



            "renderer_rules":
            {


                "semantic_html":
                True,


                "responsive":
                True,


                "mobile_first":
                True,


                "accessibility":
                True,


                "schema_ready":
                True,


                "ai_ready":
                True,


                "validation_required":
                True

            },



            "page_count":
            len(pages),


            "pages":
            pages

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
            "HTML PRODUCTION RENDERER GRAPH CREATED"
        )


        print(
            "PAGES:",
            len(pages)
        )



if __name__ == "__main__":

    HTMLProductionRenderer().build()
