import json
from engine.pipeline.content_pipeline import ContentPipeline


pipeline = ContentPipeline()


with open(
    "data_master/catalog/product_master_44.json",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


products = catalog.get(
    "products",
    []
)


results = []


for product in products:

    try:

        result = pipeline.process(
            product.copy()
        )


        results.append(
            {
                "product_id":
                    product.get("product_id"),

                "status":
                    result.get("status"),

                "related_count":
                    len(
                        result.get(
                            "related_products",
                            []
                        )
                    )
            }
        )


    except Exception as e:

        results.append(
            {
                "product_id":
                    product.get("product_id"),

                "status":
                    "ERROR",

                "error":
                    str(e)
            }
        )


print(
    json.dumps(
        results,
        indent=2,
        ensure_ascii=False
    )
)
