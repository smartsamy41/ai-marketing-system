import uuid
from datetime import datetime


def generate_affiliate_link(product):

    try:
        if not isinstance(product, dict):
            product = {}

        source = (product.get("source") or "").lower()
        product_id = product.get("product_id") or "unknown"

        if "amazon" in source:
            return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"

        if "check24" in source:
            return f"https://check24.de/vergleich/{product_id}?tracking=AI_AGENT"

        if "tarifcheck" in source:
            return f"https://tarifcheck.de/{product_id}?partner=165274"

        if "telekom" in source:
            return f"https://telekom.de/{product_id}"

        return f"https://track.ai/{product_id}?ref={uuid.uuid4()}"

    except Exception:
        return "https://fallback.ai/error"


def inject_monetization(content, product, assets):

    try:
        # =========================
        # SAFE TYPE CHECKS
        # =========================
        if not isinstance(content, dict):
            content = {}

        if not isinstance(product, dict):
            product = {}

        if not isinstance(assets, dict):
            assets = {}

        # =========================
        # SAFE CONTENT READ
        # =========================
        text = content.get("text") or ""
        title = content.get("title") or product.get("name") or product.get("product_id") or "Produkt"

        # =========================
        # LINK GENERATION
        # =========================
        affiliate_link = generate_affiliate_link(product)

        # =========================
        # FINAL OUTPUT
        # =========================
        return {
            "title": title,
            "text": f"{text}\n\n👉 Jetzt vergleichen: {affiliate_link}",
            "affiliate_link": affiliate_link,
            "tracking_id": str(uuid.uuid4()),
            "timestamp": str(datetime.now()),
            "status": "MONETIZED_OK"
        }

    except Exception as e:

        return {
            "status": "MONETIZATION_FAILED_SAFE",
            "error": str(e),
            "fallback": True,
            "timestamp": str(datetime.now())
        }
