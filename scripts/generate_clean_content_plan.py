import os
import json
from datetime import datetime


INPUT = "audits/compliance_backup_before_fix.json"
OUTPUT = "audits/clean_content_plan.json"


RULES = {
    "avoid": [
        "beste",
        "günstig",
        "sparen",
        "garantiert",
        "unabhängig",
        "objektiv"
    ],
    "use": [
        "prüfen",
        "vergleichen",
        "Kriterien betrachten",
        "Angebote bewerten",
        "Informationen einholen"
    ]
}


with open(
    INPUT,
    encoding="utf-8"
) as f:
    backup = json.load(f)


plan = {
    "created": datetime.utcnow().isoformat(),
    "rules": RULES,
    "products": [],
    "landingpages": []
}


for tab, rows in backup["tabs"].items():

    for row in rows:

        row_id = (
            row.get("product_id")
            or row.get("lp_id")
            or ""
        )

        if not row_id:
            continue


        plan[tab].append(
            {
                "id": row_id,
                "action": "REWRITE",
                "reason": "Compliance cleanup",
                "fields": list(row.keys())
            }
        )


with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        plan,
        f,
        indent=2,
        ensure_ascii=False
    )


print("CONTENT PLAN READY")
print(OUTPUT)
