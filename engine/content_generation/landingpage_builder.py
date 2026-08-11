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


        facts = facts or {}


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


        partner = product.get(
            "partner",
            ""
        )



        summary = product.get(
            "summary",
            ""
        )



        questions = product.get(
            "questions",
            []
        )


        faq = product.get(
            "faq",
            []
        )


        sources = product.get(
            "sources",
            []
        )


        key_facts = product.get(
            "key_facts",
            []
        )



        related_products = (

            related_products

            or

            product.get(
                "related_products",
                []
            )

        )



        slug = (

            name.lower()

            .replace(
                " ",
                "-"
            )

            .replace(
                "ä",
                "ae"
            )

            .replace(
                "ö",
                "oe"
            )

            .replace(
                "ü",
                "ue"
            )

        )



        entity = product.get(
            "entity",
            {}
        )



        entity_html = ""


        if entity:

            entity_html = f"""

<section class="box">

<h2>Information zur Entität</h2>

<p>
{entity}
</p>

</section>

"""




        facts_html = ""


        if key_facts:


            facts_html = """

<section class="box">

<h2>Wichtige Fakten</h2>

<ul>

"""


            for fact in key_facts:

                facts_html += (
                    f"<li>{fact}</li>"
                )


            facts_html += """

</ul>

</section>

"""




        questions_html = ""


        if questions:


            questions_html = """

<section class="box">

<h2>Fragen und Antworten</h2>

"""


            for q in questions:


                questions_html += f"""

<h3>
{q.get('question','')}
</h3>

<p>
{q.get('answer','')}
</p>

"""


            questions_html += """

</section>

"""




        faq_html = ""


        if faq:


            faq_html = """

<section class="box">

<h2>FAQ</h2>

"""


            for item in faq:


                faq_html += f"""

<h3>
{item.get('question','')}
</h3>

<p>
{item.get('answer','')}
</p>

"""


            faq_html += """

</section>

"""




        sources_html = ""


        if sources:


            sources_html = """

<section class="box">

<h2>Fakten und Quellen</h2>

<ul>

"""


            for source in sources:

                sources_html += (

                    f"<li>{source}</li>"

                )


            sources_html += """

</ul>

</section>

"""




        related_html = ""


        if related_products:


            related_html = """

<section class="box">

<h2>Verwandte Themen</h2>

<ul>

"""


            for item in related_products:

                related_html += (

                    f"<li>{item}</li>"

                )


            related_html += """

</ul>

</section>

"""




        schema = json.dumps(

            {

                "@context":
                    "https://schema.org",

                "@type":
                    "WebPage",

                "name":
                    name,

                "description":
                    summary,

                "author":
                    {

                        "@type":
                            "Organization",

                        "name":
                            "Free Basics"

                    }

            },

            ensure_ascii=False,

            indent=2

        )




        return {


            "product_id":
                product_id,


            "title":
                name,


            "description":
                summary,


            "canonical_url":
                f"https://freebasics.online/lp/{product_id}",



            "page_schema":
                schema,



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



            "content":

                f"""

<section class="box">

<h2>Direktantwort</h2>

<p>
{summary}
</p>

</section>


<section class="box">

<h2>Produktinformationen</h2>

<p>
{name} gehört zum Bereich {category}.
</p>

</section>


{entity_html}

{facts_html}

{questions_html}

{faq_html}

{sources_html}

{related_html}

""",



            "tracking_url":

                product.get(
                    "tracking_url",
                    "#"
                ),



            "affiliate_label":

                "Werbung / Anzeige",



            "footer":

                get_eeat_footer(),



            "cookie_consent":

                get_cookie_consent_script(),



            "newsletter":

                "",



            "cluster":

                product.get(
                    "cluster",
                    category
                ),



            "internal_links":

                ""

        }




    def render(
        self,
        landingpage
    ):


        return self.renderer.render(

            "landingpages/geo_optimized_landingpage.html",

            landingpage

        )
