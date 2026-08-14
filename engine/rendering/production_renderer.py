import json

from engine.template_renderer import TemplateRenderer
from engine.schema_graph.schema_graph_builder import SchemaGraphBuilder



class ProductionRenderer:


    def __init__(self):

        self.renderer = TemplateRenderer()

        self.schema = SchemaGraphBuilder()



    def _build_faq_html(
        self,
        faq
    ):

        html = []

        for item in faq or []:

            if isinstance(item, dict):

                html.append(
                    f"""
                    <div class="faq-item">
                        <h3>{item.get("question","")}</h3>
                        <p>{item.get("answer","")}</p>
                    </div>
                    """
                )

            else:

                html.append(
                    f"""
                    <div class="faq-item">
                        <p>{item}</p>
                    </div>
                    """
                )

        return "\n".join(html)



    def _build_sources_html(
        self,
        sources
    ):

        html = []

        for source in sources or []:

            if isinstance(source, dict):

                html.append(
                    f"<li>{source.get('name','')}</li>"
                )

            else:

                html.append(
                    f"<li>{source}</li>"
                )

        return "\n".join(html)



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


            "sources":

                self._build_sources_html(

                    landingpage.get(
                        "sources",
                        []
                    )

                ),



            "faq":

                self._build_faq_html(

                    landingpage.get(
                        "faq",
                        []
                    )

                ),



            # Related Products kommen bereits fertig aus LandingPageBuilder
            # keine zweite Umwandlung mehr


            "related_products":

                landingpage.get(
                    "related_products",
                    ""
                ),



            "page_schema":

                schema_json,



            "schema_json":

                schema_json,



            "tracking_url":

                landingpage.get(
                    "tracking_url",
                    "#"
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



            "sources":

                self._build_sources_html(

                    article.get(
                        "sources",
                        []
                    )

                ),



            "faq":

                self._build_faq_html(

                    article.get(
                        "faq",
                        []
                    )

                ),



            "related_products":

                article.get(
                    "related_products",
                    ""
                ),



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
