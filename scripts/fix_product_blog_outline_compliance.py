import os
import sys
import json
import ast


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
    "die besten": "geeignete",
    "der beste": "geeignete",
    "das beste": "geeignete",
    "beste": "geeignete",
    "günstige": "geeignete",
    "günstig": "geeignet",
    "geld sparen": "Kosten vergleichen",
    "sparen": "Kosten prüfen"
}


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


rows = sheets.read_records(
    "products",
    "A:ZZ"
)


changes = []


for row in rows:

    product_id = row.get("product_id","")

    outline = row.get("blog_outline")

    if not outline:
        continue


    text = str(outline)


    new_text = text


    for old,new in REPLACEMENTS.items():
        new_text = new_text.replace(old,new)
        new_text = new_text.replace(
            old.capitalize(),
            new.capitalize()
        )


    if new_text != text:

        changes.append(
            {
                "product_id": product_id,
                "old": text,
                "new": new_text
            }
        )


print("CHANGES:", len(changes))

for c in changes:
    print("="*50)
    print(c["product_id"])
    print("OLD:", c["old"])
    print("NEW:", c["new"])
