from datetime import datetime
import random

# =========================
# 🎯 ORCHESTRATOR ENGINE
# =========================

def run_orchestrator(products, learning_data=None):

    schedule = {
        "morning": [],
        "midday": [],
        "evening": []
    }

    for product in products:

        score = product.get("score", 50)
        source = product.get("source")
        product_id = product.get("product_id")

        # -------------------------
        # 🧠 AI PRIORITY BOOST (learning optional)
        # -------------------------
        if learning_data:
            for entry in learning_data:
                if entry.get("product_id") == product_id:
                    score += entry.get("boost", 0)

        # -------------------------
        # ⏰ TIME SLOT DECISION
        # -------------------------
        if score >= 85:
            slot = "morning"
        elif score >= 70:
            slot = "midday"
        else:
            slot = "evening"

        # -------------------------
        # 📌 PLATFORM STRATEGY
        # -------------------------
        if source == "amazon":
            platforms = ["pinterest", "youtube"]
        elif source == "check24":
            platforms = ["youtube", "pinterest", "blog"]
        elif source == "tarifcheck":
            platforms = ["blog", "pinterest", "youtube"]
        elif source == "telekom":
            platforms = ["shop"]
        else:
            platforms = ["pinterest"]

        # -------------------------
        # 🛡️ ANTI SPAM RULE
        # -------------------------
        if len(schedule[slot]) >= 5:
            slot = "evening"

        # -------------------------
        # FINAL TASK
        # -------------------------
        schedule[slot].append({
            "product_id": product_id,
            "source": source,
            "score": round(score, 2),
            "platforms": platforms,
            "time": datetime.now().isoformat(),
            "status": "SCHEDULED"
        })

    return {
        "status": "success",
        "mode": "ORCHESTRATOR_V1",
        "schedule": schedule,
        "summary": {
            "morning": len(schedule["morning"]),
            "midday": len(schedule["midday"]),
            "evening": len(schedule["evening"])
        }
    }
