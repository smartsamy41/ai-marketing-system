import json
import os
from datetime import datetime

DATA_FILE = "/tmp/learning_data.json"


def _load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def _save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def update_score(score, clicks, sales):
    click_weight = 0.05
    sales_weight = 5

    score_change = (clicks * click_weight) + (sales * sales_weight)

    if sales > 0:
        score_change += 5

    if clicks > 50 and sales == 0:
        score_change -= 3

    new_score = score + score_change
    new_score = max(0, min(100, new_score))

    data = _load_data()

    data.append({
        "time": datetime.now().isoformat(),
        "old_score": score,
        "new_score": new_score,
        "clicks": clicks,
        "sales": sales,
        "delta": score_change
    })

    _save_data(data)

    return round(new_score, 2)


def learn_from_results(product, tracking):
    old_score = float(product.get("score", 50))

    clicks = int(tracking.get("clicks", 0)) if isinstance(tracking, dict) else 0
    sales = int(tracking.get("sales", 0)) if isinstance(tracking, dict) else 0

    new_score = update_score(old_score, clicks, sales)

    return {
        "learning": "updated",
        "product_id": product.get("product_id"),
        "old_score": old_score,
        "new_score": new_score
    }


def get_top_products(limit=5):
    data = _load_data()
    items = [d for d in data if "new_score" in d]
    return sorted(items, key=lambda x: x["new_score"], reverse=True)[:limit]


def get_learning_summary():
    data = _load_data()
    scores = [d.get("new_score", 0) for d in data if "new_score" in d]
    avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "total_events": len(data),
        "average_score": round(avg_score, 2),
        "status": "LEARNING_ACTIVE"
    }
