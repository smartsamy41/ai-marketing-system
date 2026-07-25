import json
import os

from engine.google_sheets_live import GoogleSheetsLive


OUTPUT = "knowledge/entities/products.json"


def main():

    sheet_id = os.environ.get(
        "GOOGLE_SHEET_ID"
    )

    credentials = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_JSON"
    )


    if not sheet_id:
        raise Exception(
            "GOOGLE_SHEET_ID fehlt"
        )

    if not credentials:
        raise Exception(
            "GOOGLE_APPLICATION_CREDENTIALS_JSON fehlt"
        )


    sheets = GoogleSheetsLive(
        spreadsheet_id=sheet_id,
        credentials_json=credentials
    )


    products = sheets.read_records(
        "products",
        "A:ZZ"
    )


    entities = []


    for product in products:

        product_id = str(
            product.get("product_id","")
        ).strip()


        if not product_id:
            continue


        entities.append({

            "product_id":
                product_id,

            "name":
                product.get(
                    "product_name",
                    ""
                ),

            "partner":
                product.get(
                    "source",
                    ""
                ),

            "category":
                product.get(
                    "category",
                    ""
                ),

            "landingpage":
                product.get(
                    "landingpage_url",
                    ""
                ),

            "tracking_url":
                product.get(
                    "tracking_url_v3",
                    ""
                ),

            "system_source":
                product.get(
                    "final_system_source",
                    ""
                ),

            "status":
                product.get(
                    "status",
                    ""
                )

        })


    registry = {

        "version":
            "1.0",

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "description":
            "Product Entity Registry for GEO and Knowledge Graph",

        "status":
            "ACTIVE",

        "count":
            len(entities),

        "products":
            entities

    }


    with open(
        OUTPUT,
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
        "ENTITY IMPORT COMPLETE"
    )

    print(
        "Products:",
        len(entities)
    )


if __name__ == "__main__":
    main()
