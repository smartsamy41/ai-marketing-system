import os
import csv
import sys
from datetime import datetime


sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from engine.google_sheets_live import GoogleSheetsLive


FORBIDDEN = [
    "beste",
    "günstig",
    "sparen",
    "garantiert",
    "profitieren",
    "objektiver Vergleich",
    "unabhängig"
]


OUTPUT = "audits/forbidden_details.csv"


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


tabs = [
    "products",
    "landingpages"
]


results = []


for tab in tabs:

    print("CHECK:", tab)

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

            text = str(value).lower()


            for term in FORBIDDEN:

                if term.lower() in text:

                    results.append(
                        {
                            "tab": tab,
                            "id": row_id,
                            "field": field,
                            "term": term,
                            "value": str(value)[:300],
                            "time": datetime.utcnow().isoformat()
                        }
                    )

                    break



os.makedirs(
    "audits",
    exist_ok=True
)


with open(
    OUTPUT,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "tab",
            "id",
            "field",
            "term",
            "value",
            "time"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


print()
print("DONE")
print("FOUND:", len(results))
print("FILE:", OUTPUT)
