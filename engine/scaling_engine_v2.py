# =========================
# 📈 SCALING ENGINE V2
# =========================

def calculate_scaling(product):
    score = product.get("score", 0)

    if score >= 90:
        return {
            "budget_multiplier": 2.0,
            "action": "AGGRESSIVE_SCALE"
        }

    elif score >= 80:
        return {
            "budget_multiplier": 1.5,
            "action": "NORMAL_SCALE"
        }

    else:
        return {
            "budget_multiplier": 1.0,
            "action": "NO_SCALE"
        }
