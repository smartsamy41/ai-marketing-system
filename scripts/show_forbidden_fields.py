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


TERM = "beste"


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


for tab, key in [
    ("products", "CHK24_001"),
    ("landingpages", "CHK24_001"),
    ("products", "TEL_001"),
    ("landingpages", "TEL_001")
]:

    print("=" * 60)
    print("TAB:", tab)
    print("ID:", key)

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

        if row_id == key:

            print()

            for field, value in row.items():

                if TERM in str(value).lower():

                    print("FIELD:", field)
                    print("VALUE:", value)

            print()
            break
