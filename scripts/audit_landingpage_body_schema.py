import os

from engine.google_sheets_live import GoogleSheetsLive


def count_product(text):
    return text.count('"@type": "Product"')


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

        html = row.get("html","")

        print("LANDINGPAGE HTML")
        print("Product count:", count_product(html))

        print("HTML length:", len(html))

        break


print("DONE")
