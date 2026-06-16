import random
from datetime import datetime

def simulate_pinterest_post(product):

    score = product.get("score", 80)

    # Simulated performance based on score
    clicks = int(score * random.uniform(0.8, 2.5))
    saves = int(clicks * random.uniform(0.2, 0.6))
    impressions = int(clicks * random.uniform(10, 40))

    performance = {
        "product_id": product["product_id"],
        "time": datetime.now().strftime("%H:%M"),
        "impressions": impressions,
        "clicks": clicks,
        "saves": saves,
        "ctr": round((clicks / impressions) * 100, 2),
        "status": "SIMULATED_PIN"
    }

    return performance
