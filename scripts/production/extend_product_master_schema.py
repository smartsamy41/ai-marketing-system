import json
from pathlib import Path
from datetime import datetime, timezone


FILE = Path(
    "data_master/catalog/product_master_44.json"
)


with open(FILE, encoding="utf-8") as f:
    data = json.load(f)


for product in data.get("products", []):

    product.setdefault(
        "hero_title",
        product.get("name", "")
    )

    product.setdefault(
        "summary",
        ""
    )

    product.setdefault(
        "key_facts",
        []
    )

    product.setdefault(
        "comparison_matrix",
        []
    )

    product.setdefault(
        "faq",
        []
    )

    product.setdefault(
        "sources",
        []
    )

    product.setdefault(
        "author",
        "Redaktion Free Basics"
    )

    product.setdefault(
        "reviewed_by",
        "Samy ben Chedli Jendoubi"
    )

    product.setdefault(
        "updated_at",
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    product.setdefault(
        "entity",
        {
            "wikidata_id": "",
            "sameAs": []
        }
    )

    product.setdefault(
        "internal_links",
        []
    )


with open(
    FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        indent=2,
        ensure_ascii=False
    )


print(
    "PRODUCT MASTER EXTENDED:",
    len(data["products"])
)
