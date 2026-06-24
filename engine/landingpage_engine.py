from datetime import datetime


# =========================
# LANDINGPAGE ENGINE V1
# =========================
def generate_landingpage(product_id, data=None):

    if data is None:
        data = {}

    base_url = "https://freebasics-online.blogspot.com"

    landingpage = {
        "product_id": product_id,
        "url": f"{base_url}/p/{product_id}.html",
        "title": f"Tarif & Produkt Vergleich {product_id}",
        "created_at": datetime.utcnow().isoformat(),
        "sections": {
            "intro": "Vergleiche Tarife und finde passende Angebote",
            "cta": "Tarife prüfen",
            "affiliate_blocks": [
                "check24",
                "tarifcheck",
                "amazon"
            ]
        },
        "tracking": {
            "source": "ai_orchestrator_v1"
        }
    }

    return landingpage
