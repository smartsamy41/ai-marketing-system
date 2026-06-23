
from datetime import datetime
import random

from app.engine.landingpage_engine import generate_landingpage
from app.engine.blogger_publisher_engine import publish_blog
from app.engine.youtube_engine_v1 import create_youtube_content
from app.engine.tracking_engine import log_event


# =========================
# MAIN ORCHESTRATOR
# =========================
def run_orchestrator(job):

    product_id = job.get("product_id")
    category = job.get("category")
    data = job.get("data", {})

    hour = datetime.now().hour

    # =========================
    # SMART TIME DECISION
    # =========================
    if 6 <= hour < 12:
        slot = "MORNING"
    elif 12 <= hour < 18:
        slot = "MIDDAY"
    else:
        slot = "EVENING"

    # =========================
    # ROUTING LOGIC (NO SPAM)
    # =========================

    result = {
        "product_id": product_id,
        "slot": slot,
        "actions": []
    }

    # -------------------------
    # 1. LANDINGPAGE (ALWAYS CHECK)
    # -------------------------
    lp_url = generate_landingpage(product_id, data)

    result["actions"].append({
        "type": "landingpage",
        "url": lp_url
    })

    # -------------------------
    # 2. BLOG POST (CONTROLLED)
    # -------------------------
    if slot == "MORNING" and random.random() < 0.6:
        blog_url = publish_blog(product_id, lp_url, data)

        result["actions"].append({
            "type": "blog",
            "url": blog_url
        })

    # -------------------------
    # 3. YOUTUBE (LOW FREQUENCY = NO SPAM)
    # -------------------------
    if slot in ["MIDDAY", "EVENING"] and random.random() < 0.4:
        yt_url = create_youtube_content(product_id, lp_url, data)

        result["actions"].append({
            "type": "youtube",
            "url": yt_url
        })

    # -------------------------
    # 4. CROSS LINKING LOGIC
    # -------------------------
    result["cross_links"] = [
        "check24",
        "tarifcheck",
        "amazon"
    ]

    # -------------------------
    # 5. TRACK EVERYTHING
    # -------------------------
    log_event(result)

    return result
