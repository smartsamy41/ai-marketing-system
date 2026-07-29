from engine.template_renderer import TemplateRenderer
from engine.self_learning_agent.internal_linking_optimizer import InternalLinkingOptimizer

from datetime import datetime, timezone
import json

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



    def build(
        self,
        product,
        related_products=None,
        facts=None
    ):

        now = datetime.now(
            timezone.utc
        ).strftime("%Y-%m-%d")


        product_id = product.get(
            "product_id",
            ""
        )


        name = product.get(
            "name",
            "Angebot"
        )


        category = product.get(
            "category",
            ""
        )


        slug = (
            name.lower()
            .replace(" ", "-")
            .replace("ö","oe")
            .replace("ä","ae")
            .replace("ü","ue")
        )


        partner = product.get(
            "partner",
            ""
        )


        # Telekom bleibt externe Shop Weiterleitung
        external_shop = False

        if partner.lower() == "telekom":
            external_shop = True



        link_result = self.link_optimizer.suggest_links(

            {
                "slug": slug,
                "category": category
            },

            related_products or []

        )



        newsletter_segment = (
            category.lower()
            .replace(" ","_")
        )



        return {


            "product_id":
                product_id,


            "title":
                name,


            "category":
                category,


            "partner":
                partner,


            "landingpage_url":
                f"https://freebasics.online/angebote/{product_id}",


            "article_url":
                f"https://freebasics.online/blog/{slug}-ratgeber",



            "tracking_url":
                product.get(
                    "tracking_url",
                    ""
                ),



            "external_shop":
                external_shop,


            "shop_url":
                product.get(
                    "shop_url",
                    ""
                ),



            "description":
                product.get(
                    "summary",
                    "Informationen und Wissensartikel."
                ),



            "content":
                product.get(
                    "content",
                    "Weitere Informationen zum Angebot."
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



            "internal_links":
                link_result,



            "newsletter_enabled":
                True,


            "newsletter_segment":
                newsletter_segment,


            "newsletter_topic":
                f"Neue Informationen zu {category}",



            "facts":
                facts or {},



            "author":
                product.get(
                    "author",
                    "Redaktion Free Basics"
                ),



            "reviewer":
                product.get(
                    "reviewed_by",
                    "Free Basics Qualitätsprüfung"
                ),



            "updated_at":
                product.get(
                    "updated_at",
                    now
                ),



            "status":
                "ready_for_review",



            "system":
                self.system

        }



    def render(
        self,
        page
    ):


        schema = {


            "@context":
                "https://schema.org",


            "@type":
                "WebPage",


            "name":
                page.get(
                    "title"
                ),


            "url":
                page.get(
                    "landingpage_url"
                ),


            "about":
                page.get(
                    "category"
                )


        }



        sources_html = "\n".join(

            f"<li>{x}</li>"

            for x in page.get(
                "sources",
                []
            )

        )



        internal_html = ""

        for link in page.get(
            "internal_links",
            {}
        ).get(
            "links",
            []
        ):


            internal_html += f"""

<div class="internal-link">

<a href="/blog/{link.get('to')}-ratgeber">

{link.get('reason')}:
{link.get('to')}

</a>

</div>

"""



        faq_html = ""

        for item in page.get(
            "faq",
            []
        ):

            faq_html += f"""
<div class="faq-item">

<h3>{item.get("question","")}</h3>

<p>{item.get("answer","")}</p>

</div>
"""


        newsletter_html = """

<section class="newsletter-box">

<h3>
Newsletter
</h3>

<p>
Neue Ratgeber und Informationen erhalten.
</p>

<a href="/newsletter">
Newsletter Anmeldung
</a>

</section>

"""



        return self.renderer.render(

            "landingpages/geo_optimized_landingpage.html",

            {

                **page,


                "canonical_url":
                    page.get(
                        "landingpage_url"
                    ),


                "internal_links":
                    internal_html,


                "newsletter":
                    newsletter_html,

                "faq":
                    faq_html,


                "sources":
                    sources_html,


                "footer":
                    get_eeat_footer(),


                "cookie_consent":
                    get_cookie_consent_script(),


                "page_schema":
                    json.dumps(
                        schema,
                        indent=2,
                        ensure_ascii=False
                    )

            }

        )



    def validate(
        self,
        page
    ):


        required = [

            "product_id",
            "title",
            "landingpage_url",
            "updated_at"

        ]


        missing = [

            x

            for x in required

            if not page.get(x)

        ]


        return {


            "valid":
                len(missing)==0,


            "missing":
                missing

        }



if __name__ == "__main__":


    builder = LandingPageBuilder()


    page = builder.build(

        {

            "product_id":
                "CHK24_001",

            "name":
                "Strom",

            "category":
                "strom",

            "partner":
                "check24"

        },


        related_products=[

            {

                "product_id":
                    "TC_001",

                "category":
                    "solaranlage"

            }

        ]

    )


    print(
        builder.validate(page)
    )


    print(
        builder.render(page)[:1000]
    )

