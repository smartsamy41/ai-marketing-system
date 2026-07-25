import json


class GEOSchemaGenerator:

    def __init__(
        self,
        context="https://schema.org"
    ):
        self.context = context


    def product_schema(
        self,
        product
    ):

        return {
            "@context": self.context,
            "@type": "Product",
            "name": product.get("name"),
            "category": product.get("category"),
            "brand": {
                "@type": "Organization",
                "name": product.get("partner")
            },
            "productID": product.get("product_id")
        }


    def article_schema(
        self,
        article
    ):

        return {
            "@context": self.context,
            "@type": "Article",
            "headline": article.get("title"),
            "author": {
                "@type": "Organization",
                "name": article.get(
                    "author",
                    "Free Basics Redaktion"
                )
            },
            "datePublished": article.get(
                "published_at"
            ),
            "dateModified": article.get(
                "updated_at"
            ),
            "about": article.get(
                "product_id"
            )
        }


    def faq_schema(
        self,
        questions
    ):

        return {
            "@context": self.context,
            "@type": "FAQPage",
            "mainEntity": questions
        }


    def to_json_ld(
        self,
        schema
    ):

        return json.dumps(
            schema,
            ensure_ascii=False,
            indent=2
        )


if __name__ == "__main__":

    generator = GEOSchemaGenerator()

    schema = generator.product_schema(
        {
            "name": "Strom",
            "category": "Energie",
            "partner": "check24",
            "product_id": "CHK24_001"
        }
    )

    print(
        generator.to_json_ld(schema)
    )
