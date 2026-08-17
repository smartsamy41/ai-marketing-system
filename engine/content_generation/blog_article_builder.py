import json

from engine.template_renderer import TemplateRenderer


class BlogArticleBuilder:


    def __init__(self):

        self.renderer = TemplateRenderer()



    def build(
        self,
        product,
        facts=None,
        related_products=None
    ):


        facts = facts or {}

        related_products = (
            related_products
            or []
        )


        questions = product.get(
            "questions",
            []
        )


        sources = product.get(
            "sources",
            []
        )


        name = product.get(
            "name",
            ""
        )


        description = product.get(
            "summary",
            ""
        )



        content = ""


        content += f"""

<section>

<h2>Direktantwort</h2>

<p>
{name} einfach erklärt:
{description}
</p>

</section>

"""



        content += """

<section>

<h2>Grundlagen und Informationen</h2>

<p>
Hier finden Sie wichtige Informationen,
Zusammenhänge und Kriterien zum Thema.
</p>

</section>

"""



        key_facts = product.get(
            "key_facts",
            []
        )


        if key_facts:


            content += """

<section>

<h2>Wichtige Fakten</h2>

<ul>

"""


            for fact in key_facts:

                content += (
                    f"<li>{fact}</li>"
                )


            content += """

</ul>

</section>

"""



        if questions:


            content += """

<section>

<h2>Fragen und Antworten</h2>

"""


            for q in questions:

                content += f"""

<h3>
{q.get('question','')}
</h3>

<p>
{q.get('answer','')}
</p>

"""


            content += """

</section>

"""




        faq_html = ""


        faq = product.get(
            "faq",
            []
        )


        if faq:


            for item in faq:


                faq_html += f"""

<h3>
{item.get('question','')}
</h3>

<p>
{item.get('answer','')}
</p>

"""





        source_html = ""


        if sources:

            source_html += """
            <li>
            Diese Seite basiert auf hinterlegten Partnerinformationen.
            </li>
            """


            for source in sources:

                source_html += (
                    f"<li>Quelle: {source}</li>"
                )

        else:

            source_html += """
            <li>
            Keine zusätzlichen Quellen hinterlegt.
            </li>
            """


        related_html = ""


        for item in related_products:


            related_html += (

                f"<li>{item}</li>"

            )




        schema = json.dumps(

            {

                "@context":
                    "https://schema.org",

                "@type":
                    "Article",

                "headline":
                    name,

                "author":
                    {

                        "@type":
                            "Person",

                        "name":
                            product.get(
                                "author",
                                "Redaktion Free Basics"
                            )

                    },

                "description":
                    description

            },

            ensure_ascii=False,

            indent=2

        )





        article = {


            "title":
                name,


            "description":
                description,


            "ai_summary":
                description,


            "direct_answer":
                f"""
                <p>
                {name} einfach erklärt:
                {description}
                </p>
                """,


            "content":
                content,


            "entity_context":
                """
                <p>
                Dieser Artikel basiert auf hinterlegten Wissensdaten
                und geprüften Informationsquellen.
                </p>
                """,


            "sources":
                source_html,


            "questions":
                faq_html,


            "faq":
                faq_html,


            "related_products":
                related_html,


            "internal_links":
                "",


            "affiliate_area":
                f"""
                <p>
                Dieser Bereich enthält ein externes Partnerangebot.
                </p>

                <a href="{product.get('tracking_url','#')}"
                   target="_blank"
                   rel="sponsored nofollow noopener">

                   Vergleich starten

                </a>
                """,


            "newsletter":
                """
                <p>
                Neue Ratgeber und Informationen von Free Basics erhalten.
                </p>
                """,


            "footer":
                "",


            "article_schema":
                schema,


            "faq_schema":
                "",


            "canonical_url":
                product.get(
                    "article_url",
                    ""
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
                product.get(
                    "updated_at",
                    ""
                )


        }


        return article




    def render(
        self,
        article
    ):


        return self.renderer.render(

            "blog/geo_authority_article.html",

            article

        )
