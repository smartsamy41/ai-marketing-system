import os
import sys


sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from engine.google_sheets_live import GoogleSheetsLive


REPLACEMENTS = {
    "beste": "passende",
    "günstig": "geeignet",
    "sparen": "Kosten prüfen",
    "Geld sparen": "Kosten vergleichen"
}


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


for tab in [
    "products",
    "landingpages"
]:

    print("=" * 60)
    print("TAB:", tab)


    rows = sheets.read_records(
        tab,
        "A:ZZ"
    )


    for row in rows:

        row_id = (
            row.get("product_id")
            or row.get("lp_id")
            or ""
        )


        for field, value in row.items():

            text = str(value)

            for old, new in REPLACEMENTS.items():

                if old.lower() in text.lower():

                    print()
                    print("ID:", row_id)
                    print("FIELD:", field)
                    print("ALT:", old)
                    print("NEU:", new)
                    print("TEXT:", text[:200])
                    print("-" * 40)

                    break
