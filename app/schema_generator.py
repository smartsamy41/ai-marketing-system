import json


def generate_product_schema(
    name: str,
    description: str,
    url: str,
    product_id: str = "",
    partner: str = "",
    category: str = "",
    status: str = "active"
) -> str:

    schema = {

        "@context": "https://schema.org",

        "@type": "Product",

        "name": name,

        "description": description,

        "url": url,

        "additionalProperty": [

            {
                "@type": "PropertyValue",
                "name": "Product ID",
                "value": product_id
            },

            {
                "@type": "PropertyValue",
                "name": "Partner",
                "value": partner
            },

            {
                "@type": "PropertyValue",
                "name": "Category",
                "value": category
            },

            {
                "@type": "PropertyValue",
                "name": "GEO Status",
                "value": status
            }

        ]

    }


    return (
        '<script type="application/ld+json">'
        +
        json.dumps(
            schema,
            ensure_ascii=False
        )
        +
        '</script>'
    )



def generate_article_schema(
    title: str,
    description: str,
    url: str,
    date_published: str
) -> str:

    schema = {

        "@context": "https://schema.org",

        "@type": "Article",

        "headline": title,

        "description": description,

        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },

        "datePublished": date_published,

        "author": {
            "@type": "Organization",
            "name": "Free Basics Redaktion"
        },

        "publisher": {
            "@type": "Organization",
            "name": "Free Basics"
        }

    }


    return (
        '<script type="application/ld+json">'
        +
        json.dumps(
            schema,
            ensure_ascii=False
        )
        +
        '</script>'
    )
