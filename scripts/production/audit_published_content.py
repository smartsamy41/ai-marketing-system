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

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-")



with open(
    CATALOG,
    encoding="utf-8"
) as f:

    catalog=json.load(f)



expected_lp=set()
expected_article=set()



for product in catalog["products"]:

    slug=slugify(
        product["name"]
    )

    expected_lp.add(
        slug+".html"
    )

    expected_article.add(
        slug+"-ratgeber.html"
    )



print("="*60)
print("PUBLISHED CONTENT AUDIT")
print("="*60)



print()
print("EXPECTED LANDINGPAGES:",len(expected_lp))
print("EXPECTED ARTICLES:",len(expected_article))



print()
print("EXTRA LANDINGPAGES:")

for f in sorted(LP_DIR.iterdir()):

    if f.name not in expected_lp:

        print(
            "OLD:",
            f.name
        )



print()
print("EXTRA ARTICLES:")

for f in sorted(ARTICLE_DIR.iterdir()):

    if f.name not in expected_article:

        print(
            "OLD:",
            f.name
        )



print()
print("="*60)
print("AUDIT COMPLETE")
print("="*60)
