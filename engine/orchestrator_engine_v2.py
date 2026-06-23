from datetime import datetime
import random


# =========================
# SAFE IMPORTS (FAIL PROTECTED)
# =========================
try:
    from app.engine.landingpage_engine import generate_landingpage
    from app.engine.blogger_publisher_engine import publish_blog
    from app.engine.youtube_engine_v1 import create_youtube_content
    from app.engine.tracking_engine import log_event
except Exception as e:
    def generate_landingpage(*args, **kwargs):
        return "ERROR_LANDINGPAGE_IMPORT"

    def publish_blog(*args, **kwargs):
        return "ERROR_BLOG_IMPORT"

    def create_youtube_content(*args, **kwargs):
        return "ERROR_YOUTUBE_IMPORT"

    def log_event(*args, **kwargs):
        print("LOG_DISABLED:", e)


# =========================
# ORCHESTRATOR V2
# =========================
def run_orchestrator(job):

    product_id = job.get("product_id")
    category = job.get("category", "default")
    data = job.get("data", {})

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

        log_event(result)
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
    lp_url = generate_landingpage(product_id, data)

    result["actions"].append({
        "type": "landingpage",
        "url": lp_url
    })

    # =========================
    # BLOG (CONTROLLED)
    # =========================
    if slot == "MORNING" and random.random() < 0.6:
        blog_url = publish_blog(product_id, lp_url, data)

        result["actions"].append({
            "type": "blog",
            "url": blog_url
        })

    # =========================
    # YOUTUBE (LOW FREQUENCY)
    # =========================
    if slot in ["MIDDAY", "EVENING"] and random.random() < 0.4:
        yt_url = create_youtube_content(product_id, lp_url, data)

        result["actions"].append({
            "type": "youtube",
            "url": yt_url
        })

    # =========================
    # CROSS LINKS
    # =========================
    result["cross_links"] = [
        "check24",
        "tarifcheck",
        "amazon"
    ]

    # =========================
    # TRACKING SAFE CALL
    # =========================
    log_event(result)

    return result
