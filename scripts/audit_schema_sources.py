import os
import re

from engine.google_sheets_live import GoogleSheetsLive


def count_product(text):
    return text.count('"@type": "Product"')


print("=" * 50)
print("SCHEMA SOURCE AUDIT")
print("=" * 50)


# Google Sheet prüfen

sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)

rows = sheets.read_records(
    "landingpages",
    "A:ZZ"
)


for row in rows:

    if row.get("product_id") == "CHK24_001":

        print("\nSHEET landingpages")
        print("product_id:", row.get("product_id"))

        print(
            "html Product:",
            count_product(row.get("html",""))
        )

        print(
            "structured_data Product:",
            count_product(row.get("structured_data",""))
        )


# Code prüfen

files = [
    "app/main.py",
    "app/schema_generator.py",
    "app/product_templates.py"
]


print("\nCODE FILES")

for file in files:

    try:
        data = open(
            file,
            encoding="utf-8"
        ).read()

        print(
            file,
            "Product:",
            count_product(data)
        )

    except Exception as e:
        print(
            file,
            e
        )


print("\nAUDIT COMPLETE")
