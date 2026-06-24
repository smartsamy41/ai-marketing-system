from datetime import datetime
import random


def run_orchestrator(job):

    product_id = job.get("product_id")
    category = job.get("category", "default")
    data = job.get("data", {})

    # =========================
    # FIX: hour DEFINIERT
    # =========================
    hour = datetime.now().hour

    # =========================
    # TIME SLOT
    # =========================
    if 6 <= hour < 12:
        slot = "MORNING"
    elif 12 <= hour < 18:
        slot = "MIDDAY"
    else:
        slot = "EVENING"

    result = {
        "product_id": product_id,
        "category": category,
        "slot": slot,
        "actions": [],
        "cross_links": []
    }

    # =========================
    # TELEKOM ROUTE
    # =========================
    if category == "telekom":
        result["actions"].append({
            "type": "telekom_redirect",
            "target": "official_shop"
        })
        return result

    # =========================
    # AMAZON ROUTE
    # =========================
    if category == "amazon":
        result["actions"].append({
            "type": "amazon_cross_link",
            "target": "affiliate"
        })

    # =========================
    # LANDINGPAGE
    # =========================
    result["actions"].append({
        "type": "landingpage",
        "url": f"/landing/{product_id}"
    })

    # =========================
    # BLOG (SAFE RANDOM)
    # =========================
    if slot == "MORNING" and random.random() < 0.6:
        result["actions"].append({
            "type": "blog",
            "url": f"/blog/{product_id}"
        })

    # =========================
    # YOUTUBE (SAFE RANDOM)
    # =========================
    if slot in ["MIDDAY", "EVENING"] and random.random() < 0.4:
        result["actions"].append({
            "type": "youtube",
            "url": f"/youtube/{product_id}"
        })

    # =========================
    # CROSS LINKS
    # =========================
    result["cross_links"] = [
        "check24",
        "tarifcheck",
        "amazon"
    ]

    return result
