import os
import json
import urllib.request
from datetime import datetime

from engine.google_sheets_live import GoogleSheetsLive


OUTPUT = "audits/live_geo_audit_report.json"

SITE_URL = "https://freebasics.online"


FORBIDDEN_TERMS = [
    "garantiert",
    "beste",
    "unabhängig",
    "objektiver vergleich",
    "wir übernehmen",
    "günstig sparen"
]


def fetch(url):

    try:
        with urllib.request.urlopen(
            url,
            timeout=15
        ) as response:

            return response.read().decode(
                "utf-8",
                errors="ignore"
            )

    except Exception as e:

        return f"ERROR: {e}"


def count_product_schema(html):

    return html.count(
        '"@type": "Product"'
    )


def check_forbidden(html):

    found = []

    text = html.lower()

    for term in FORBIDDEN_TERMS:

        if term.lower() in text:
            found.append(term)

    return found



def main():

    print("=" * 60)
    print("FREE BASICS GEO LIVE AUDIT")
    print("=" * 60)


    sheets = GoogleSheetsLive(
        spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
        credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
    )


    products = sheets.read_records(
        "products",
        "A:ZZ"
    )


    results = []


    for product in products:

        product_id = str(
            product.get("product_id","")
        ).strip()


        if not product_id:
            continue


        url = f"{SITE_URL}/lp/{product_id}"


        print(
            "CHECK:",
            product_id
        )


        html = fetch(url)


        product_count = count_product_schema(
            html
        )


        forbidden = check_forbidden(
            html
        )


        status = "OK"


        if product_count != 1:
            status = "SCHEMA_ERROR"


        if forbidden:
            status = "COMPLIANCE_WARNING"


        results.append({

            "product_id":
                product_id,

            "url":
                url,

            "schema_product_count":
                product_count,

            "schema_status":
                "CLEAN"
                if product_count == 1
                else "ERROR",

            "forbidden_terms":
                forbidden,

            "status":
                status

        })


    report = {

        "system":
            "FREE BASICS AI MARKETING SYSTEM",

        "audit":
            "LIVE GEO PRODUCTION AUDIT",

        "generated_at":
            datetime.utcnow().isoformat(),

        "products_checked":
            len(results),

        "results":
            results

    }


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
            report,
            f,
            indent=2,
            ensure_ascii=False
        )


    print()
    print("=" * 60)
    print("AUDIT COMPLETE")
    print("Products:", len(results))
    print("Report:", OUTPUT)
    print("=" * 60)



if __name__ == "__main__":
    main()
