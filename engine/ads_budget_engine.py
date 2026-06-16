import random

# -----------------------------
# 💰 BUDGET DECISION ENGINE
# -----------------------------
def calculate_budget(product):

    score = product.get("score", 80)

    if score >= 95:
        budget = random.randint(50, 100)
        level = "HIGH_SCALE"

    elif score >= 85:
        budget = random.randint(20, 50)
        level = "MEDIUM_SCALE"

    elif score >= 70:
        budget = random.randint(5, 20)
        level = "TEST"

    else:
        budget = 0
        level = "STOP"

    return {
        "product_id": product["product_id"],
        "score": score,
        "budget": budget,
        "level": level,
        "status": "ADS_READY"
    }


# -----------------------------
# 📊 SIMULATE ROI
# -----------------------------
def simulate_roi(budget, clicks, sales):

    if budget == 0:
        return {
            "roi": 0,
            "status": "NO_SPEND"
        }

    revenue = sales * 15
    cost = budget

    roi = ((revenue - cost) / cost) * 100

    return {
        "roi": round(roi, 2),
        "revenue": revenue,
        "cost": cost,
        "status": "ROI_CALCULATED"
    }


# -----------------------------
# 🔥 ADS DECISION
# -----------------------------
def decide_ads(product, clicks=0, sales=0):

    budget_data = calculate_budget(product)

    roi_data = simulate_roi(
        budget_data["budget"],
        clicks,
        sales
    )

    return {
        "product_id": product["product_id"],
        "ads": budget_data,
        "roi": roi_data
    }
