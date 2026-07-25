from pathlib import Path
import json


PRODUCT_FILE = Path(
    "data_master/catalog/product_master_44.json"
)


def get_landingpage(product_id):

    data = json.loads(
        PRODUCT_FILE.read_text(
            encoding="utf-8"
        )
    )

    for product in data.get("products", []):

        if product.get("product_id") == product_id:

            return {
                "product_id": product_id,
                "name": product.get("name"),
                "landingpage": product.get("landingpage"),
                "status": "found"
            }

    return {
        "product_id": product_id,
        "status": "not_found"
    }
