# =========================
# 🧠 WINNER ENGINE V2
# =========================

def decide_winner(product):
    """
    Simple but smarter decision logic
    """

    score = product.get("score", 0)

    if score >= 90:
        return {
            "action": "WINNER",
            "confidence": "HIGH",
            "reason": "Top Performance"
        }

    elif score >= 80:
        return {
            "action": "KEEP",
            "confidence": "MEDIUM",
            "reason": "Stable Performance"
        }

    else:
        return {
            "action": "LOW_PRIORITY",
            "confidence": "LOW",
            "reason": "Weak Performance"
        }
