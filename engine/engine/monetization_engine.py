import uuid
from datetime import datetime

# =========================
# 💰 MONETIZATION ENGINE V1
# =========================

def generate_affiliate_link(product, assets):

    try:

        base_source = product.get("source", "generic")
        product_id = product.get("product_id")

        # =========================
        # AMAZON
        # =========================
        if "amazon" in base_source.lower():

            return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"

        # =========================
        # CHECK24 / TARIFCHECK
        # =========================
        if "check24" in base_source.lower():

            return f"https://check24.de/vergleich/{product_id}?tracking=AI_AGENT"

        if "tarifcheck" in base_source.lower():

            return f"https://tarifcheck.de/{product_id}?partner=165274"

        # =========================
        # DEFAULT
        # =========================
        return f"https://track.ai/{product_id}?ref={uuid.uuid4()}"

    except Exception as e:

        return f"https://fallback.ai/error"


# =========================
# 💰 APPLY MONETIZATION TO CONTENT
# =========================

def inject_monetization(content, product, assets):

    try:

        affiliate_link = generate_affiliate_link(product, assets)

        monetized_content = {
            "title": content.get("title"),
            "text": content.get("text") + f"\n\n👉 Jetzt vergleichen: {affiliate_link}",
            "affiliate_link": affiliate_link,
            "tracking_id": str(uuid.uuid4()),
            "timestamp": str(datetime.now())
        }

        return monetized_content

    except Exception as e:

        return {
            "error": str(e),
            "status": "monetization_failed"
        }
