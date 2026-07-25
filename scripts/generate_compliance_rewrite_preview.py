import os
import json
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


INPUT = "audits/compliance_backup_before_fix.json"
OUTPUT = "audits/clean_rewrite_preview.json"


FORBIDDEN = [
    "beste",
    "günstig",
    "sparen",
    "garantiert",
    "unabhängig",
    "objektiv"
]


def clean_text(text):

    if not text:
        return text

    replacements = {
        "beste": "passende",
        "Beste": "Passende",

        "günstig": "geeignet",
        "Günstig": "Geeignet",

        "sparen": "Kosten prüfen",
        "Sparen": "Kosten prüfen",

        "garantiert": "geprüft",
        "Garantiert": "Geprüft"
    }

    result = text

    for old, new in replacements.items():

        result = result.replace(
            old,
            new
        )

    return result



def contains_forbidden(text):

    if not text:
        return []

    found = []

    lower = str(text).lower()

    for term in FORBIDDEN:

        if term.lower() in lower:
            found.append(term)

    return found



with open(
    INPUT,
    encoding="utf-8"
) as f:

    backup = json.load(f)



preview = {

    "created": datetime.utcnow().isoformat(),

    "mode": "PREVIEW_ONLY",

    "products": [],

    "landingpages": []

}



for tab in [
    "products",
    "landingpages"
]:

    rows = backup["tabs"].get(
        tab,
        []
    )


    for row in rows:


        row_id = (
            row.get("product_id")
            or row.get("lp_id")
            or ""
        )


        if not row_id:
            continue


        item = {

            "id": row_id,

            "changes": []

        }


        for field, value in row.items():


            forbidden = contains_forbidden(
                str(value)
            )


            if forbidden:


                new_value = clean_text(
                    str(value)
                )


                item["changes"].append(

                    {
                        "field": field,

                        "found": forbidden,

                        "old": str(value)[:1000],

                        "new_preview": new_value[:1000]

                    }

                )


        if item["changes"]:

            preview[tab].append(
                item
            )



os.makedirs(
    "audits",
    exist_ok=True
)



with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        preview,
        f,
        indent=2,
        ensure_ascii=False
    )


print("="*60)
print("COMPLIANCE REWRITE PREVIEW READY")
print("="*60)
print("FILE:")
print(OUTPUT)

print()

print(
    "PRODUCT CHANGES:",
    len(preview["products"])
)

print(
    "LANDINGPAGE CHANGES:",
    len(preview["landingpages"])
)
