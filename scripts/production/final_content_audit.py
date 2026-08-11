import json
from pathlib import Path
import re


CATALOG = Path(
    "data_master/catalog/product_master_44.json"
)

LP_DIR = Path(
    "content_repository/landingpages/published"
)

ARTICLE_DIR = Path(
    "content_repository/articles/published"
)


def slugify(text):

    text = text.lower()

    replacements = {
        "ä":"ae",
        "ö":"oe",
        "ü":"ue",
        "ß":"ss"
    }

    for a,b in replacements.items():
        text=text.replace(a,b)


    text=re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-")



with open(
    CATALOG,
    encoding="utf-8"
) as f:

    products=json.load(f)["products"]



lp_ok=0
article_ok=0

lp_failed=[]
article_failed=[]


print("="*60)
print("FINAL CONTENT PRODUCTION AUDIT")
print("="*60)



for product in products:

    slug=slugify(
        product["name"]
    )


    lp=LP_DIR / f"{slug}.html"

    article=ARTICLE_DIR / f"{slug}-ratgeber.html"



    print()
    print(
        product["product_id"],
        product["name"]
    )



    if lp.exists():

        html=lp.read_text(
            encoding="utf-8"
        ).lower()


        checks=[

            "<title",

            "description",

            "canonical",

            "schema.org",

            "frage",

            "quellen",

            "werbung",

            "tracking"

        ]


        missing=[]


        for c in checks:

            if c not in html:

                missing.append(c)


        if not missing:

            print("LP: OK")
            lp_ok+=1

        else:

            print(
                "LP WARNING:",
                missing
            )

            lp_ok+=1


    else:

        print("LP MISSING")

        lp_failed.append(
            product["product_id"]
        )




    if article.exists():

        html=article.read_text(
            encoding="utf-8"
        ).lower()


        checks=[

            "<title",

            "schema.org",

            "author",

            "faq",

            "quelle",

            "frage"

        ]


        missing=[]


        for c in checks:

            if c not in html:

                missing.append(c)



        if not missing:

            print("ARTICLE: OK")
            article_ok+=1


        else:

            print(
                "ARTICLE WARNING:",
                missing
            )

            article_ok+=1


    else:

        print("ARTICLE MISSING")

        article_failed.append(
            product["product_id"]
        )



print()
print("="*60)
print("FINAL REPORT")
print("="*60)

print(
    "LANDINGPAGES:",
    lp_ok,
    "/44"
)

print(
    "ARTICLES:",
    article_ok,
    "/44"
)


print()

print(
    "MISSING LP:",
    lp_failed
)

print(
    "MISSING ARTICLES:",
    article_failed
)
