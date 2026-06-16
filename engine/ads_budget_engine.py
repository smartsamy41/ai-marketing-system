import random

# =============================
# 💰 ADS BUDGET ENGINE V2
# =============================

MAX_DAILY_BUDGET = 100
MIN_TEST_BUDGET = 5


def calculate_budget(product):
    score = product.get("score", 80)

    if score >= 95:
        budget = random.randint(50, MAX_DAILY_BUDGET)
        level = "HIGH_SCALE"
        action = "SCALE"

    elif score >= 85:
        budget = random.randint(20, 50)
        level = "MEDIUM_SCALE"
        action = "RUN_TEST"

    elif score >= 70:
        budget = random.randint(MIN_TEST_BUDGET, 20)
        level = "TEST"
        action = "TEST_ONLY"

    else:
        budget = 0
        level = "STOP"
        action = "DO_NOT_SPEND"

    return {
        "product_id": product["product_id"],
        "score": score,
        "budget": budget,
        "currency": "EUR",
        "level": level,
        "action": action,
        "status": "ADS_READY"
    }


def simulate_roi(budget, clicks, sales, avg_commission=15):
    if budget <= 0:
        return {
            "roi": 0,
            "revenue": 0,
            "cost": 0,
            "profit": 0,
            "status": "NO_SPEND"
        }

    revenue = sales * avg_commission
    cost = budget
    profit = revenue - cost
    roi = (profit / cost) * 100

    return {
        "roi": round(roi, 2),
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "status": "ROI_CALCULATED"
    }


def decide_ads(product, clicks=0, sales=0):
    budget_data = calculate_budget(product)

    roi_data = simulate_roi(
        budget_data["budget"],
        clicks,
        sales
    )

    if roi_data["roi"] > 50:
        final_decision = "INCREASE_BUDGET"
    elif roi_data["roi"] >= 0:
        final_decision = "KEEP_TESTING"
    elif budget_data["budget"] == 0:
        final_decision = "NO_ADS"
    else:
        final_decision = "REDUCE_OR_STOP"

    return {
        "product_id": product["product_id"],
        "ads": budget_data,
        "roi": roi_data,
        "final_decision": final_decision
    }
