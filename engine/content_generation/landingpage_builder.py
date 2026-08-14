from engine.template_renderer import TemplateRenderer
from engine.self_learning_agent.internal_linking_optimizer import InternalLinkingOptimizer

from datetime import datetime, timezone

from app.templates.base_components import (
    get_eeat_footer,
    get_cookie_consent_script
)


class LandingPageBuilder:


    def __init__(
        self,
        system="FREE BASICS AI MARKETING SYSTEM"
    ):

        self.system = system
        self.renderer = TemplateRenderer()
        self.link_optimizer = InternalLinkingOptimizer()



    def _slugify(
        self,
        text
    ):

        return (
            str(text)
            .lower()
            .replace(" ", "-")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
        )



    def _build_related_products_html(
        self,
        products
    ):

        html = []

        for item in (products or [])[:8]:

            if isinstance(item, dict):

                category = item.get(
                    "category",
                    item.get(
                        "product_id",
                        ""
                    )
                )


                slug = self._slugify(
                    category
                )


                html.append(
                    f"""
                    <div class="related-product">
                        <a href="/angebote/{slug}">
                            {category}
                        </a>
                    </div>
                    """
                )


            else:

                html.append(
                    f"""
                    <div class="related-product">
                        {item}
                    </div>
                    """
                )


        return "\n".join(html)



    def build(
        self,
        product,
        related_products=None,
        facts=None
    ):


        now = datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d"
        )


        name = product.get(
            "name",
            "Angebot"
        )


        category = product.get(
            "category",
            ""
        )



        resolved_related_products = (

            related_products

            or

            product.get(
                "related_products",
                []
            )

        )



        related_html = self._build_related_products_html(
            resolved_related_products
        )



        slug = self._slugify(
            name
        )



        internal_links = self.link_optimizer.suggest_links(

            {
                "slug": slug,
                "category": category
            },

            resolved_related_products

        )



        return {


            "system":
                self.system,


            "product_id":
                product.get(
                    "product_id",
                    ""
                ),



            "title":
                name,



            "category":
                category,



            "partner":
                product.get(
                    "partner",
                    ""
                ),



            "cluster":
                product.get(
                    "cluster",
                    category
                ),



            "silo":
                product.get(
                    "silo",
                    ""
                ),



            "product_type":
                product.get(
                    "product_type",
                    ""
                ),



            "related_products":
                related_html,



            "description":
                product.get(
                    "summary",
                    ""
                ),



            "content":
                product.get(
                    "content",
                    ""
                ),



            "faq":
                product.get(
                    "faq",
                    []
                ),



            "questions":
                product.get(
                    "questions",
                    []
                ),



            "sources":
                product.get(
                    "sources",
                    []
                ),



            "knowledge_depth":
                product.get(
                    "knowledge_depth",
                    {}
                ),



            "content_experience":
                product.get(
                    "content_experience",
                    {}
                ),



            "production_page_architecture":
                product.get(
                    "production_page_architecture",
                    {}
                ),



            "asset_selection":
                product.get(
                    "asset_selection",
                    []
                ),



            "production_validation":
                product.get(
                    "production_validation",
                    {}
                ),



            "tracking_url":
                product.get(
                    "tracking_url",
                    "#"
                ),



            "author":
                product.get(
                    "author",
                    "Redaktion Free Basics"
                ),



            "reviewed_by":
                product.get(
                    "reviewed_by",
                    ""
                ),



            "updated_at":
                now,



            "canonical_url":
                f"https://freebasics.online/angebote/{slug}",



            "internal_links":
                internal_links.get(
                    "links",
                    []
                ),



            "footer":
                get_eeat_footer(),



            "cookie_consent":
                get_cookie_consent_script()

        }



    def render(
        self,
        landingpage
    ):

        return self.renderer.render(

            "landingpages/geo_optimized_landingpage.html",

            landingpage

        )
