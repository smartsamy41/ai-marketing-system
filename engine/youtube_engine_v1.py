from datetime import datetime
import random


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe(v):
    return str(v or "").strip()


def generate_youtube_title(product):
    name = _safe(product.get("product_name"))
    source = _safe(product.get("source"))

    hooks = [
        "2026 Vergleich",
        "Top Angebot jetzt prüfen",
        "So sparst du wirklich Geld",
        "Preis Check aktuell",
        "Beste Wahl in Deutschland"
    ]

    return f"{name} - {random.choice(hooks)}"


def generate_description(product, landingpage_url, affiliate_url):
    name = _safe(product.get("product_name"))

    return f"""
{name} Vergleich 2026

👉 Jetzt vergleichen: {landingpage_url or affiliate_url}

⚠️ Werbung / Anzeige. Affiliate Link enthalten.

#Vergleich #Sparen #Angebote
""".strip()


def route_youtube(product, routing_result):
    source = _safe(product.get("source")).lower()

    # TELEKOM DIRECT
    if source == "telekom" or product.get("product_id", "").startswith("TEL_"):
        return {
            "channel": "youtube",
            "upload_type": "shorts",
            "target_url": routing_result.get("target_url"),
            "status": "DIRECT_TO_SHOP"
        }

    # DEFAULT LANDINGPAGE FLOW
    return {
        "channel": "youtube",
        "upload_type": "shorts",
        "target_url": routing_result.get("target_url"),
        "status": "LANDINGPAGE_FLOW"
    }


def build_youtube_entry(product, routing_result):
    product_id = _safe(product.get("product_id"))

    target_url = routing_result.get("target_url")

    title = generate_youtube_title(product)
    description = generate_description(product, target_url, target_url)

    return {
        "youtube_id": f"YT_{product_id}",
        "product_id": product_id,
        "title": title,
        "description": description,
        "target_url": target_url,
        "status": "READY_FOR_UPLOAD",
        "created_at": _now(),
        "upload_status": "pending"
    }


def process_youtube_queue(products, routing_engine):
    results = []

    for product in products:
        try:
            routing = routing_engine.route_product(product)

            yt = build_youtube_entry(product, routing)

            results.append({
                "product_id": product.get("product_id"),
                "routing": routing,
                "youtube": yt,
                "status": "OK"
            })

        except Exception as e:
            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "YOUTUBE_ENGINE_V1_DONE",
        "executed": len(results),
        "results": results,
        "timestamp": _now()
    }


class YouTubeEngineV1:
    def __init__(self):
        print("🟢 YouTube Engine V1 loaded")

    def run(self, products, routing_engine):
        return process_youtube_queue(products, routing_engine)
