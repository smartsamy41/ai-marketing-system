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


def track_event(product, output):
    data = _load()

    entry = {
        "time": datetime.now().isoformat(),
        "product_id": product.get("product_id"),
        "source": product.get("source"),
        "channel": output.get("channel"),
        "output_status": output.get("status", "prepared"),
        "clicks": 0,
        "impressions": 0,
        "sales": 0
    }

    data.append(entry)
    _save(data)

    return {
        "tracked": True,
        "product_id": entry["product_id"],
        "channel": entry["channel"]
    }


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


def get_product_stats(product_id):
    data = _load()
    filtered = [d for d in data if d.get("product_id") == product_id]

    clicks = sum(d.get("clicks", 0) for d in filtered)
    impressions = sum(d.get("impressions", 0) for d in filtered)
    sales = sum(d.get("sales", 0) for d in filtered)

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


def get_top_products(limit=5):
    data = _load()
    scores = {}

    for d in data:
        pid = d.get("product_id")
        if not pid:
            continue

        if pid not in scores:
            scores[pid] = {
                "clicks": 0,
                "sales": 0,
                "impressions": 0
            }

        scores[pid]["clicks"] += d.get("clicks", 0)
        scores[pid]["sales"] += d.get("sales", 0)
        scores[pid]["impressions"] += d.get("impressions", 0)

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

    return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
