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


        for source in sources:


            source_html += (

                f"<li>{source}</li>"

            )



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


            "content":
                content,


            "faq":
                faq_html,


            "sources":
                source_html,


            "related_products":
                related_html,


            "article_schema":
                schema,


            "ai_summary":
                description,


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
