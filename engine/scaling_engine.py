from datetime import datetime

# =========================
# 📈 SCALING ENGINE V1 (FIXED)
# =========================

def calculate_scaling(product, metrics):

    score = product.get("score", 0)
    clicks = metrics.get("clicks", 0)
    sales = metrics.get("sales", 0)

    if score >= 90 and sales > 0:
        action = "SCALE_UP"
        multiplier = 2.5
        level = "AGGRESSIVE"

    elif score >= 80 and clicks > 10:
        action = "SCALE_UP"
        multiplier = 1.5
        level = "GROWTH"

    elif score >= 70:
        action = "HOLD"
        multiplier = 1.0
        level = "STABLE"

    else:
        action = "SCALE_DOWN"
        multiplier = 0.3
        level = "CUT"

    return {
        "product_id": product.get("product_id"),
        "score": score,
        "clicks": clicks,
        "sales": sales,
        "action": action,
        "budget_multiplier": multiplier,
        "level": level,
        "timestamp": datetime.now().isoformat()
    }
