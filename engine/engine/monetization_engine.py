import uuid
from datetime import datetime


def generate_affiliate_link(product):

    try:
        if not isinstance(product, dict):
            return "https://fallback.ai/error"

        source = str(product.get("source") or "").strip().lower()
        product_id = str(product.get("product_id") or "unknown")

        # =========================
        # AMAZON
        # =========================
        if "amazon" in source:
            return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"

        # =========================
        # CHECK24
        # =========================
        if "check24" in source:
            return f"https://check24.de/vergleich/{product_id}?tracking=AI_AGENT"

        # =========================
        # TARIFCHECK
        # =========================
        if "tarifcheck" in source:
            return f"https://tarifcheck.de/{product_id}?partner=165274"

        # =========================
        # TELEKOM
        # =========================
        if "telekom" in source:
            return f"https://telekom.de/{product_id}"

        # =========================
        # FALLBACK
        # =========================
        return f"https://track.ai/{product_id}?ref={uuid.uuid4()}"

    except Exception:
        return "https://fallback.ai/error"


def inject_monetization(content, product, assets):

    try:
        # =========================
        # SAFE INPUTS
        # =========================
        content = content if isinstance(content, dict) else {}
        product = product if isinstance(product, dict) else {}
        assets = assets if isinstance(assets, dict) else {}

        # =========================
        # SAFE READ
        # =========================
        text = content.get("text") or ""
        title = (
            content.get("title")
            or product.get("name")
            or product.get("product_id")
            or "Produkt"
        )

        # =========================
        # LINK
        # =========================
        affiliate_link = generate_affiliate_link(product)

        # =========================
        # OUTPUT
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
