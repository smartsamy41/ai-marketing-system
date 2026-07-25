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


OUTPUT = "audits/forbidden_content_source_audit.csv"


def main():

    sheets = GoogleSheetsLive(
        spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
        credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
    )


    tabs = [
        "products",
        "landingpages",
        "blog_posts",
        "content_queue",
        "pin_queue"
    ]


    results = []


    for tab in tabs:

        print("=" * 50)
        print("CHECK:", tab)

        try:

            rows = sheets.read_records(
                tab,
                "A:ZZ"
            )

        except Exception as e:

            print("SKIP:", e)
            continue


        for row in rows:

            text = str(row).lower()


            for term in FORBIDDEN:

                if term.lower() in text:

                    results.append(
                        {
                            "tab": tab,
                            "id":
                                row.get("product_id")
                                or row.get("lp_id")
                                or row.get("article_id")
                                or row.get("queue_id")
                                or "",
                            "term": term,
                            "timestamp": datetime.utcnow().isoformat()
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
                "term",
                "timestamp"
            ]
        )

        writer.writeheader()
        writer.writerows(results)


    print()
    print("=" * 50)
    print("COMPLIANCE SOURCE AUDIT COMPLETE")
    print("FOUND:", len(results))
    print("REPORT:", OUTPUT)
    print("=" * 50)


if __name__ == "__main__":
    main()
eof
