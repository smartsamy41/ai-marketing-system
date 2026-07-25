import os

from engine.google_sheets_live import GoogleSheetsLive


TERM = "beste"


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


for tab in [
    "products",
    "landingpages",
    "blog_articles"
]:

    print("=" * 60)
    print("TAB:", tab)

    try:
        rows = sheets.read_records(tab, "A:ZZ")

        for row in rows:

            text = str(row).lower()

            if TERM in text:

                print()
                print("FOUND")
                print("ID:", row.get("product_id") or row.get("lp_id") or row.get("article_id"))
                print(row)

    except Exception as e:
        print("ERROR:", e)
