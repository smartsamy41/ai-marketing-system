import json
from pathlib import Path


INPUT_FILE = Path(
    "data_master/geo_and_entities/entity_registry/product_facts_registry.json"
)

OUTPUT_FILE = Path(
    "data_master/geo_and_entities/entity_registry/entity_relationships.json"
)


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        registry = json.load(f)


    relationships = []


    for product in registry["products"]:

        relationships.append(

            {
                "from_entity":
                    "Free Basics",

                "relation":
                    "offers_information_about",

                "to_entity":
                    product.get("name"),


                "product_id":
                    product.get("product_id"),


                "category":
                    product.get("category"),


                "partner":
                    product.get("partner"),


                "source":
                    product.get("source"),


                "status":
                    "active"

            }

        )


    output = {

        "version":
            "1.0",


        "system":
            "FREE BASICS AI MARKETING SYSTEM",


        "description":
            "Entity Relationship Registry",


        "relationships":
            relationships,


        "count":
            len(relationships),


        "status":
            "ACTIVE"

    }


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        "CREATED:",
        OUTPUT_FILE
    )

    print(
        "RELATIONSHIPS:",
        len(relationships)
    )


if __name__ == "__main__":
    main()
