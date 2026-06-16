from engine.tracking_engine import get_top_products
from engine.winner_detection_engine import detect_winners


def build_dashboard():

    top_products = get_top_products()

    winners = detect_winners([
        {"product_id": p["product_id"], "score": p["score"]}
        for p in top_products
    ])

    return {
        "status": "LIVE_DASHBOARD",
        "top_products": top_products,
        "winners": winners,
        "insights": {
            "mode": "AUTO_LEARNING",
            "recommendation": "SCALE_TOP_PRODUCTS"
        }
    }


def get_summary():

    top = get_top_products()

    total_score = sum([p.get("score", 0) for p in top])
    avg_score = total_score / len(top) if top else 0

    return {
        "average_score": round(avg_score, 2),
        "products_count": len(top),
        "status": "DASHBOARD_OK"
    }
