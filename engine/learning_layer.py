from datetime import datetime

# =========================
# 🧠 LEARNING LAYER V1
# =========================

# In-Memory Speicher (später: BigQuery / Sheets)
LEARNING_DB = []


def log_decision(product, winner, scaling):
    """
    Speichert jede AI Entscheidung für Learning
    """

    entry = {
        "timestamp": datetime.now().isoformat(),
        "product_id": product.get("product_id"),
        "score": product.get("score"),
        "winner_action": winner.get("action"),
        "winner_reason": winner.get("reason"),
        "scaling_action": scaling.get("action"),
        "budget_multiplier": scaling.get("budget_multiplier"),
    }

    LEARNING_DB.append(entry)

    return entry


def get_learning_data():
    """
    Gibt gespeicherte Learnings zurück
    """

    return {
        "total_decisions": len(LEARNING_DB),
        "data": LEARNING_DB[-50:]  # letzte 50
    }


def analyze_learning():
    """
    Simple AI Learning Analyse (V1)
    """

    if not LEARNING_DB:
        return {
            "status": "NO_DATA",
            "insight": "Not enough data to learn"
        }

    scale_up_count = len([x for x in LEARNING_DB if x["scaling_action"] == "SCALE_UP"])
    keep_count = len([x for x in LEARNING_DB if x["winner_action"] == "KEEP"])

    return {
        "status": "ACTIVE_LEARNING",
        "total_records": len(LEARNING_DB),
        "scale_up_ratio": round(scale_up_count / len(LEARNING_DB), 2),
        "keep_ratio": round(keep_count / len(LEARNING_DB), 2),
        "insight": "System learns from scaling vs keep decisions"
    }
