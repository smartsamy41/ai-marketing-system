import json
from pathlib import Path


PRODUCT_FILE = Path(
    "data_master/catalog/product_master_44.json"
)

OUTPUT_FILE = Path(
    "data_master/geo_and_entities/entity_registry/product_facts_registry.json"
)


def main():

    with open(
        PRODUCT_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        catalog = json.load(f)


    products = []


    for product in catalog["products"]:

        products.append(

            {

                "product_id":
                    product.get("product_id"),


                "name":
                    product.get("name"),


                "category":
                    product.get("category"),


                "partner":
                    product.get("partner"),


                "source":
                    product.get("partner"),


                "knowledge_graph":

                    {

                        "wikidata_id":
                            None,

                        "google_mid":
                            None,

                        "status":
                            "pending_verification"

                    },


                "facts_status":
                    "source_available",


                "validation":
                    {

                        "source_required":
                            True,

                        "fact_validation_required":
                            True,

                        "fabricated_information":
                            False

                    }

            }

        )


    registry = {

        "version":
            "1.0",


        "system":
            "FREE BASICS AI MARKETING SYSTEM",


        "description":
            "Product Facts Registry",


        "rules":
            {

                "source_required":
                    True,

                "fact_validation_required":
                    True,

                "no_fabricated_information":
                    True

            },


        "products":
            products,


        "count":
            len(products),


        "status":
            "ACTIVE"

    }


    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            registry,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        "CREATED:",
        OUTPUT_FILE
    )

    print(
        "PRODUCTS:",
        len(products)
    )



if __name__ == "__main__":
    main()
