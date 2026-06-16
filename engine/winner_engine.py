from datetime import datetime

# =========================
# 🏆 WINNER DETECTION ENGINE
# =========================

def detect_winners(products):
    """
    Findet Gewinner basierend auf Score + Performance
    """

    winners = []

    for p in products:

        score = p.get("score", 0)

        # WINNER RULES
        if score >= 90:
            status = "WINNER"
        elif score >= 80:
            status = "STRONG"
        elif score >= 70:
            status = "TEST"
        else:
            status = "STOP"

        winners.append({
            "product_id": p["product_id"],
            "score": score,
            "status": status,
            "time": datetime.now().isoformat()
        })

    return winners


# =========================
# ⚡ AUTO DECISION ENGINE
# =========================

def decide_action(product):

    score = product.get("score", 0)

    if score >= 90:
        return {
            "action": "SCALE",
            "budget_multiplier": 2.0,
            "reason": "HIGH_PERFORMANCE"
        }

    if score >= 80:
        return {
            "action": "KEEP",
            "budget_multiplier": 1.0,
            "reason": "STABLE"
        }

    if score >= 70:
        return {
            "action": "TEST",
            "budget_multiplier": 0.5,
            "reason": "LOWER_PERFORMANCE"
        }

    return {
        "action": "STOP",
        "budget_multiplier": 0,
        "reason": "POOR_PERFORMANCE"
    }
