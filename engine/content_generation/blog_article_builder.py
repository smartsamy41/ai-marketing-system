from engine.template_renderer import TemplateRenderer
from datetime import datetime, timezone
import json


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
            "artikel"
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
                product.get("product_id"),


            "title":
                name,


            "description":
                product.get(
                    "description",
                    "Wissensartikel zu diesem Thema."
                ),


            "category":
                product.get("category"),


            "partner":
                product.get("partner"),



            "article_url":
                f"https://freebasics.online/blog/{slug}-ratgeber",



            "author":
                "Free Basics Redaktion",


            "reviewer":
                "Free Basics Qualitätsprüfung",



            "published_at":
                now,


            "updated_at":
                now,



            "ai_summary":
                f"Zusammenfassung der wichtigsten Informationen zu {name}.",



            "content":
                product.get(
                    "content",
                    "Weitere Informationen und Wissensinhalte."
                ),



            "sources":
                """
<li>Produktdaten aus dem Master-Katalog</li>
<li>Offizielle Partnerinformationen</li>
<li>Öffentliche Wissensquellen</li>
""",



            "related_products":
                f"""
<a href="/angebote/{product.get('product_id')}">
Passendes Angebot prüfen
</a>
""",



            "faq":
                """
<ul>
<li>Was ist dieses Thema?</li>
<li>Welche Informationen sind verfügbar?</li>
<li>Wo finden Nutzer weitere Details?</li>
</ul>
""",



            "facts":
                facts or {},



            "article_schema":
                "{}",



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
                article.get("title"),


            "author":
                {
                    "@type":
                        "Organization",

                    "name":
                        "Free Basics Redaktion"
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
                article.get("published_at"),


            "dateModified":
                article.get("updated_at"),


            "mainEntityOfPage":
                {
                    "@type":
                        "WebPage",

                    "@id":
                        article.get("article_url")
                }

        }


        return self.renderer.render(
            "blog/geo_authority_article.html",
            {
                **article,

                "canonical_url":
                    article.get("article_url"),

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
            if not article.get(field)

        ]


        return {

            "valid":
                len(missing) == 0,

            "missing":
                missing

        }
