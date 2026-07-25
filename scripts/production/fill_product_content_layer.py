import json
from pathlib import Path
from datetime import datetime, timezone


FILE = Path(
    "data_master/catalog/product_master_44.json"
)


with open(FILE, encoding="utf-8") as f:
    data = json.load(f)


for product in data["products"]:

    if product["product_id"] == "CHK24_001":

        product["summary"] = (
            "Informationen zu Stromtarifen und wichtigen "
            "Kriterien wie Verbrauch, Vertragsbedingungen "
            "und Tarifdetails."
        )


        product["key_facts"] = [
            "Stromtarife anhand wichtiger Vertragsdaten prüfen",
            "Verbrauch und Tarifdetails berücksichtigen",
            "Anbieterinformationen transparent darstellen"
        ]


        product["comparison_matrix"] = [
            {
                "field": "Kategorie",
                "value": "Strom"
            },
            {
                "field": "Datenbasis",
                "value": "Produktinformationen und Partnerdaten"
            },
            {
                "field": "Status",
                "value": "aktiv"
            }
        ]


        product["faq"] = [
            {
                "question": "Was sollte bei einem Stromtarif geprüft werden?",
                "answer": "Wichtige Punkte sind Verbrauch, Vertragslaufzeit und Tarifbedingungen."
            },
            {
                "question": "Wo erfolgt die weitere Abwicklung?",
                "answer": "Die weitere Bearbeitung erfolgt über den jeweiligen Partner."
            }
        ]


        product["sources"] = [
            "Offizielle Partnerinformationen",
            "Produktdaten aus dem Free Basics Master Katalog"
        ]


        product["internal_links"] = [
            "/blog/strom-ratgeber"
        ]


        product["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()


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


print("CONTENT LAYER UPDATED")
