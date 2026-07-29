import json

from engine.template_renderer import TemplateRenderer
from engine.schema_graph.schema_graph_builder import SchemaGraphBuilder


class ProductionRenderer:


    def __init__(self):

        self.renderer = TemplateRenderer()
        self.schema = SchemaGraphBuilder()



    def render_landingpage(
        self,
        landingpage
    ):


        schema_json = json.dumps(

            self.schema.product_schema(
                landingpage
            ),

            indent=2,

            ensure_ascii=False

        )


        data = {


            **landingpage,


            "title":
                landingpage.get(
                    "title",
                    ""
                ),


            "description":
                landingpage.get(
                    "description",
                    ""
                ),


            "ai_summary":
                landingpage.get(
                    "ai_summary",
                    ""
                ),


            "introduction":
                landingpage.get(
                    "introduction",
                    ""
                ),


            "content":
                landingpage.get(
                    "content",
                    ""
                ),


            "tracking_url":
                landingpage.get(
                    "tracking_url",
                    "#"
                ),


            "sources":
                landingpage.get(
                    "sources",
                    []
                ),


            "faq":
                landingpage.get(
                    "faq",
                    []
                ),


            "author":
                landingpage.get(
                    "author",
                    "Redaktion Free Basics"
                ),


            "reviewed_by":
                landingpage.get(
                    "reviewed_by",
                    ""
                ),


            "updated_at":
                landingpage.get(
                    "updated_at",
                    ""
                ),


            "canonical_url":
                landingpage.get(
                    "canonical_url",
                    ""
                ),


            "og_image_url":
                landingpage.get(
                    "og_image_url",
                    ""
                ),


            "schema_json":
                schema_json

        }



        return self.renderer.render(

            "landingpages/geo_optimized_landingpage.html",

            data

        )



    def render_article(
        self,
        article
    ):


        article_schema = json.dumps(

            self.schema.article_schema(
                article
            ),

            indent=2,

            ensure_ascii=False

        )


        sources_html = "\n".join(
            f"<li>{source}</li>"
            for source in article.get(
                "sources",
                []
            )
        )


        data = {


            **article,


            "sources":
                sources_html,


            "canonical_url":
                article.get(
                    "article_url",
                    ""
                ),


            "article_schema":
                article_schema


        }



        return self.renderer.render(

            "blog/geo_authority_article.html",

            data

        )
