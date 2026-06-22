from datetime import datetime


# =========================
# MONEY INTELLIGENCE CORE
# =========================
def calculate_epc(clicks, revenue):

    if clicks <= 0:
        return 0.0

    return float(revenue) / float(clicks)


# =========================
# SCORE ENGINE (0–100)
# =========================
def score_product(epc, clicks, revenue):

    score = 0

    # Revenue weight
    score += min(revenue * 10, 40)

    # EPC weight
    score += min(epc * 30, 40)

    # Stability bonus (clicks)
    if clicks > 10:
        score += 20
    else:
        score += clicks * 2

    return min(score, 100)


# =========================
# DECISION ENGINE
# =========================
def decide(score):

    if score >= 70:
        return "SCALE"
    elif score >= 40:
        return "OPTIMIZE"
    else:
        return "KILL"


# =========================
# TRAFFIC ALLOCATION ENGINE
# =========================
def allocate_traffic(products):

    results = []

    for p in products:

        product_id = p.get("product_id")
        clicks = float(p.get("clicks", 0))
        revenue = float(p.get("revenue", 0))

        epc = calculate_epc(clicks, revenue)
        score = score_product(epc, clicks, revenue)
        decision = decide(score)

        traffic_boost = 1.0

        if decision == "SCALE":
            traffic_boost = 2.5
        elif decision == "OPTIMIZE":
            traffic_boost = 1.2
        else:
            traffic_boost = 0.3

        results.append({
            "product_id": product_id,
            "clicks": clicks,
            "revenue": revenue,
            "epc": epc,
            "score": score,
            "decision": decision,
            "traffic_boost": traffic_boost,
            "timestamp": str(datetime.now())
        })

    return {
        "status": "MONEY_OPTIMIZER_V3_COMPLETE",
        "results": results
    }


# =========================
# GLOBAL OPTIMIZER ENTRY
# =========================
def run_money_optimizer(products):

    return allocate_traffic(products)
