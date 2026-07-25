import json

from engine.template_renderer import TemplateRenderer
from engine.schema_graph.schema_graph_builder import SchemaGraphBuilder


class ProductionRenderer:


    def __init__(self):

        self.renderer = TemplateRenderer()
        self.schema = SchemaGraphBuilder()



    def render_landingpage(
        self,
        product
    ):

        product_schema = json.dumps(

            self.schema.product_schema(
                product
            ),

            indent=2,
            ensure_ascii=False

        )


        data = {

            **product,


            "title":
                product.get(
                    "hero_title",
                    product.get(
                        "name",
                        ""
                    )
                ),


            "description":
                product.get(
                    "summary",
                    ""
                ),


            "ai_summary":
                product.get(
                    "summary",
                    ""
                ),


            "key_facts":
                product.get(
                    "key_facts",
                    []
                ),


            "comparison_matrix":
                product.get(
                    "comparison_matrix",
                    []
                ),


            "sources":
                product.get(
                    "sources",
                    []
                ),


            "faq":
                product.get(
                    "faq",
                    []
                ),


            "author":
                product.get(
                    "author",
                    "Redaktion Free Basics"
                ),


            "reviewed_by":
                product.get(
                    "reviewed_by",
                    "Samy ben Chedli Jendoubi"
                ),


            "updated_at":
                product.get(
                    "updated_at",
                    ""
                ),


            "schema_json":
                product_schema,


            "canonical_url":
                product.get(
                    "landingpage_url",
                    "https://freebasics.online/angebote/"
                    +
                    product.get(
                        "product_id",
                        ""
                    )
                )

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


        data = {

            **article,


            "article_schema":
                article_schema,


            "author":
                article.get(
                    "author",
                    "Redaktion Free Basics"
                ),


            "reviewed_by":
                article.get(
                    "reviewed_by",
                    "Samy ben Chedli Jendoubi"
                )

        }


        return self.renderer.render(

            "blog/geo_authority_article.html",

            data

        )
