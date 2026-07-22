import json


def generate_geo_product_entity(
    product_id: str,
    name: str,
    description: str,
    url: str,
    partner: str = "",
    category: str = "",
    status: str = "active"
):

    schema = {

        "@context": "https://schema.org",

        "@type": "Product",

        "@id": url + "#product",

        "name": name,

        "description": description,

        "url": url,

        "brand": {
            "@type": "Organization",
            "name": partner
        },

        "category": category,

        "identifier": {

            "@type": "PropertyValue",

            "propertyID": "Free Basics Product ID",

            "value": product_id

        },

        "additionalProperty": [

            {
                "@type": "PropertyValue",
                "name": "GEO Status",
                "value": status
            },

            {
                "@type": "PropertyValue",
                "name": "Knowledge Graph Entity",
                "value": "FREE BASICS AI MARKETING SYSTEM"
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
