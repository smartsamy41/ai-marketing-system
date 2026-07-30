from engine.template_renderer import TemplateRenderer
from engine.self_learning_agent.internal_linking_optimizer import InternalLinkingOptimizer

from datetime import datetime, timezone
import json

from app.templates.base_components import (
    get_eeat_footer,
    get_cookie_consent_script
)


class BlogArticleBuilder:

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
        facts=None,
        related_products=None
    ):

        now = datetime.now(
            timezone.utc
        ).strftime("%Y-%m-%d")


        name = product.get(
            "name",
            "Artikel"
        )


        slug = (
            name.lower()
            .replace(" ", "-")
            .replace("ö", "oe")
            .replace("ä", "ae")
            .replace("ü", "ue")
        )


        category = product.get(
            "category",
            ""
        )


        newsletter_segment = (
            category.lower()
            .replace(" ", "_")
        )


        link_result = self.link_optimizer.suggest_links(
            {
                "slug": slug,
                "category": category
            },
            related_products or []
        )


        return {


            "product_id":
                product.get(
                    "product_id",
                    ""
                ),


            "title":
                name,


            "description":
                product.get(
                    "summary",
                    "Wissensartikel zu diesem Thema."
                ),


            "category":
                category,


            "partner":
                product.get(
                    "partner",
                    ""
                ),


            "article_url":
                f"https://freebasics.online/blog/{slug}-ratgeber",



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



            "published_at":
                product.get(
                    "published_at",
                    now
                ),



            "updated_at":
                product.get(
                    "updated_at",
                    now
                ),



            "og_image_url":
                product.get(
                    "image_url",
                    "https://freebasics.online/assets/og-default.webp"
                ),



            "ai_summary":
                product.get(
                    "summary",
                    f"Zusammenfassung der wichtigsten Informationen zu {name}."
                ),



            "content":
                product.get(
                    "content"
                )
                or
                (
                    "<section>"
                    "<h2>Informationen</h2>"
                    f"<p>{product.get('summary', '')}</p>"
                    "</section>"
                    "<section>"
                    "<h2>Wichtige Fakten</h2>"
                    "<ul>"
                    +
                    "".join(
                        f"<li>{fact}</li>"
                        for fact in product.get(
                            "key_facts",
                            []
                        )
                    )
                    +
                    "</ul>"
                    "</section>"
                    "<section>"
                    "<h2>Häufige Fragen</h2>"
                    +
                    "".join(
                        f"<p><strong>{faq.get('question','')}</strong><br>{faq.get('answer','')}</p>"
                        for faq in product.get(
                            "faq",
                            []
                        )
                    )
                    +
                    "</section>"
                ),



            "sources":
                product.get(
                    "sources",
                    []
                ),



            "link_data":
                link_result,



            "newsletter_enabled":
                True,



            "newsletter_segment":
                newsletter_segment,



            "newsletter_topic":
                f"Informationen zu {category}",



            "faq":
                product.get(
                    "faq",
                    []
                ),



            "facts":
                facts or {},



            "type":
                "blog_article",



            "status":
                "ready_for_review",



            "system":
                self.system

        }



    def render(
        self,
        article
    ):


        schema = {

            "@context":
                "https://schema.org",


            "@type":
                "Article",


            "headline":
                article.get(
                    "title"
                ),


            "author":
                {
                    "@type":
                        "Organization",

                    "name":
                        article.get(
                            "author"
                        )
                },


            "publisher":
                {
                    "@type":
                        "Organization",

                    "name":
                        "Free Basics",

                    "url":
                        "https://freebasics.online"
                },


            "datePublished":
                article.get(
                    "published_at"
                ),


            "dateModified":
                article.get(
                    "updated_at"
                ),


            "mainEntityOfPage":
                {
                    "@type":
                        "WebPage",

                    "@id":
                        article.get(
                            "article_url"
                        )
                }

        }



        sources_html = "\n".join(
            f"<li>{source}</li>"
            for source in article.get(
                "sources",
                []
            )
        )



        internal_links_html = ""


        for link in article.get(
            "link_data",
            {}
        ).get(
            "links",
            []
        ):

            internal_links_html += f"""

<div class="internal-link">

<a href="/angebote/{link.get('to')}">

{link.get('reason')}
:
{link.get('to')}

</a>

</div>

"""



        newsletter_html = """

<section class="newsletter-box">

<h3>
Newsletter
</h3>


<p>
Erhalte neue Informationen,
Ratgeber und Hinweise zu passenden Themen.
</p>


<p>
Thema:
%s
</p>


<a href="/newsletter">
Newsletter Anmeldung
</a>


</section>

""" % article.get(
            "newsletter_topic",
            ""
        )



        return self.renderer.render(

            "blog/geo_authority_article.html",

            {


                **article,



                "canonical_url":
                    article.get(
                        "article_url"
                    ),



                "sources":
                    sources_html,



                "internal_links":
                    internal_links_html,



                "newsletter":
                    newsletter_html,



                "footer":
                    get_eeat_footer(),



                "cookie_consent":
                    get_cookie_consent_script(),



                "article_schema":

                    json.dumps(
                        schema,
                        indent=2,
                        ensure_ascii=False
                    )

            }

        )




    def validate(
        self,
        article
    ):


        required = [

            "product_id",
            "title",
            "author",
            "reviewer",
            "article_url",
            "updated_at"

        ]


        missing = [

            field

            for field in required

            if not article.get(
                field
            )

        ]


        return {

            "valid":
                len(missing) == 0,


            "missing":
                missing

        }




if __name__ == "__main__":


    builder = BlogArticleBuilder()


    article = builder.build(

        {
            "product_id":
                "CHK24_001",

            "name":
                "Strom",

            "category":
                "Energie",

            "partner":
                "check24",

            "summary":
                "Informationen zu Stromtarifen"

        },


        related_products=[

            {
                "product_id":
                    "CHK24_001",

                "category":
                    "strom"

            },

            {
                "product_id":
                    "TC_001",

                "category":
                    "solaranlage"

            }

        ]

    )


    print(
        builder.validate(
            article
        )
    )


    print(
        builder.render(
            article
        )[:1000]
    )
