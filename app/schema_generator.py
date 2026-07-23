import json


def generate_product_schema(product):

    return {

        "@context": "https://schema.org",

        "@type": "Product",

        "name": product.get(
            "name",
            ""
        ),

        "description": product.get(
            "description",
            f"Informationen zu {product.get('name','Produkt')}"
        ),

        "url": product.get(
            "url",
            ""
        ),

        "productID": product.get(
            "product_id",
            ""
        ),

        "category": product.get(
            "category",
            ""
        ),

        "brand": {

            "@type": "Organization",

            "name": product.get(
                "partner",
                ""
            )

        },

        "additionalProperty": [

            {
                "@type": "PropertyValue",
                "name": "Free Basics Product ID",
                "value": product.get(
                    "product_id",
                    ""
                )
            },

            {
                "@type": "PropertyValue",
                "name": "Partner",
                "value": product.get(
                    "partner",
                    ""
                )
            },

            {
                "@type": "PropertyValue",
                "name": "Category",
                "value": product.get(
                    "category",
                    ""
                )
            },

            {
                "@type": "PropertyValue",
                "name": "GEO Status",
                "value": "active"
            }

        ]

    }
