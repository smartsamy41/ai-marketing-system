import json
import os
from datetime import datetime

TRACK_FILE = "/tmp/tracking_data.json"


def _load():
    if not os.path.exists(TRACK_FILE):
        return []

    try:
        with open(TRACK_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def _save(data):
    with open(TRACK_FILE, "w") as f:
        json.dump(data, f)


# -----------------------------
# 🟢 LOG EVENT
# -----------------------------
def log_event(product_id, clicks=0, impressions=0, sales=0, platform="unknown"):

    data = _load()

    ctr = 0
    if impressions > 0:
        ctr = round((clicks / impressions) * 100, 2)

    data.append({
        "time": datetime.now().isoformat(),
        "product_id": product_id,
        "clicks": clicks,
        "impressions": impressions,
        "sales": sales,
        "ctr": ctr,
        "platform": platform
    })

    _save(data)

    return True


# -----------------------------
# 🟢 GET PRODUCT PERFORMANCE
# -----------------------------
def get_product_stats(product_id):

    data = _load()

    filtered = [d for d in data if d["product_id"] == product_id]

    clicks = sum(d["clicks"] for d in filtered)
    impressions = sum(d["impressions"] for d in filtered)
    sales = sum(d["sales"] for d in filtered)

    ctr = 0
    if impressions > 0:
        ctr = round((clicks / impressions) * 100, 2)

    return {
        "product_id": product_id,
        "clicks": clicks,
        "impressions": impressions,
        "sales": sales,
        "ctr": ctr
    }


# -----------------------------
# 🟢 TOP PERFORMER
# -----------------------------
def get_top_products(limit=5):

    data = _load()

    scores = {}

    for d in data:
        pid = d["product_id"]

        if pid not in scores:
            scores[pid] = {
                "clicks": 0,
                "sales": 0,
                "impressions": 0
            }

        scores[pid]["clicks"] += d["clicks"]
        scores[pid]["sales"] += d["sales"]
        scores[pid]["impressions"] += d["impressions"]

    results = []

    for pid, s in scores.items():

        ctr = 0
        if s["impressions"] > 0:
            ctr = (s["clicks"] / s["impressions"]) * 100

        score = (s["sales"] * 10) + ctr

        results.append({
            "product_id": pid,
            "score": round(score, 2),
            "ctr": round(ctr, 2)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:limit]
