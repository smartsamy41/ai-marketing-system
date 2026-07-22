import json


def generate_jsonld_script(
    data: dict
) -> str:

    return (
        '<script type="application/ld+json">'
        +
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
        +
        '</script>'
    )



def build_product_jsonld(
    product: dict
) -> str:

    schema = {

        "@context":
            "https://schema.org",

        "@type":
            "Product",

        "@id":
            product.get(
                "landingpage",
                ""
            ) + "#product",

        "name":
            product.get(
                "name",
                ""
            ),

        "category":
            product.get(
                "category",
                ""
            ),

        "brand":
            {
                "@type":
                    "Organization",

                "name":
                    product.get(
                        "partner",
                        ""
                    )
            },

        "url":
            product.get(
                "landingpage",
                ""
            ),

        "identifier":
            {
                "@type":
                    "PropertyValue",

                "propertyID":
                    "Free Basics Product ID",

                "value":
                    product.get(
                        "product_id",
                        ""
                    )
            },

        "additionalProperty":
            [

                {
                    "@type":
                        "PropertyValue",

                    "name":
                        "GEO Ready",

                    "value":
                        str(
                            product.get(
                                "geo_ready",
                                False
                            )
                        )
                },

                {
                    "@type":
                        "PropertyValue",

                    "name":
                        "Asset Status",

                    "value":
                        product.get(
                            "asset_status",
                            ""
                        )
                }

            ]

    }


    return generate_jsonld_script(
        schema
    )
