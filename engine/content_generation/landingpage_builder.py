from engine.rendering.production_renderer import ProductionRenderer
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

        self.renderer = ProductionRenderer()

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




    def _build_content(
        self,
        product
    ):

        html = []


        summary = str(
            product.get(
                "summary",
                ""
            )
            or ""
        ).strip()


        if summary:

            html.append(
                f"""
                <div class="content-summary">
                    <p>{summary}</p>
                </div>
                """
            )


        facts = product.get(
            "key_facts",
            []
        )


        clean_facts = []

        for fact in facts:

            if isinstance(fact, dict):

                text = (
                    fact.get("title")
                    or fact.get("name")
                    or fact.get("description")
                    or ""
                )

            else:

                text = str(fact)


            text = text.strip()


            blocked = [
                "product_id",
                "entity_type",
                "asset_status",
                "tracking_available",
                "source_reference",
                "geo_ready"
            ]


            if text and not any(
                x in text.lower()
                for x in blocked
            ):

                clean_facts.append(
                    text
                )


        if clean_facts:

            html.append(
                """
                <h3>
                Wichtige Informationen
                </h3>

                <ul>
                """
            )


            for item in clean_facts:

                html.append(
                    f"<li>{item}</li>"
                )


            html.append(
                """
                </ul>
                """
            )


        if not html:

            html.append(
                """
                <p>
                Weitere Informationen werden
                aus geprüften Quellen ergänzt.
                </p>
                """
            )


        return "\n".join(html)


    def _build_related_products_html(
        self,
        products
    ):

        html=[]


        for item in (products or [])[:8]:

            if isinstance(item,dict):

                name=item.get(
                    "category",
                    item.get(
                        "product_id",
                        ""
                    )
                )


                slug=self._slugify(
                    name
                )


                html.append(
                    f"""
                    <div class="related-product">
                        <a href="/angebote/{slug}">
                            {name}
                        </a>
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


        now=datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d"
        )


        name=product.get(
            "name",
            product.get(
                "product_name",
                "Produkt"
            )
        )


        category=product.get(
            "category",
            ""
        )


        slug=self._slugify(
            name
        )


        internal_links=self.link_optimizer.suggest_links(
            {
                "slug":slug,
                "category":category
            },
            related_products or []
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


            "description":
                product.get(
                    "summary",
                    ""
                ),


            "content":
                self._build_content(
                    product
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


            "related_products":
                self._build_related_products_html(
                    related_products
                ),


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

        return self.renderer.render_landingpage(
            landingpage
        )
