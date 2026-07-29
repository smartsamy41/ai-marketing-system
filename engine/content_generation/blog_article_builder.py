from engine.template_renderer import TemplateRenderer
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



    def build(
        self,
        product,
        facts=None
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
                product.get(
                    "category",
                    ""
                ),


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
                    product.get(
                        "updated_at",
                        now
                    )
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
                    "content",
                    product.get(
                        "summary",
                        "Weitere Informationen und Wissensinhalte."
                    )
                ),


            "sources":
                product.get(
                    "sources",
                    []
                ),


            "related_products":
                f"""
<a href="{product.get('landingpage_url', '#')}">
Passendes Angebot prüfen
</a>
""",


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
                            "author",
                            "Redaktion Free Basics"
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



        return self.renderer.render(

            "blog/geo_authority_article.html",

            {

                **article,


                "og_image_url":
                    article.get(
                        "og_image_url",
                        "https://freebasics.online/assets/og-default.webp"
                    ),


                "footer":
                    get_eeat_footer(),


                "cookie_consent":
                    get_cookie_consent_script(),


                "sources":
                    sources_html,


                "canonical_url":
                    article.get(
                        "article_url"
                    ),


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
                "check24"

        }

    )


    print(

        builder.validate(
            article
        )

    )


    print(

        builder.render(
            article
        )[:500]

    )
