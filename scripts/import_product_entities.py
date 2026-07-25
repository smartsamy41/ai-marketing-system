import json
from pathlib import Path
from datetime import datetime


OUTPUT = "knowledge/entities/products.json"


def import_products():

    products = [

        {
            "product_id": "IMPORT_FROM_SHEET",
            "name": "",
            "partner": "",
            "category": "",
            "landingpage": "",
            "tracking": "",
            "status": "pending"
        }

    ]


    registry = {

        "version": "1.0",

        "system":
        "FREE BASICS AI MARKETING SYSTEM",

        "description":
        "Product Entity Registry for GEO and Knowledge Graph",

        "generated_at":
        datetime.utcnow().isoformat(),

        "status":
        "ACTIVE",

        "products":
        products

    }


    Path(OUTPUT).write_text(
        json.dumps(
            registry,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print("PRODUCT ENTITY IMPORT READY")
    print("Products:", len(products))


if __name__ == "__main__":
    import_products()
