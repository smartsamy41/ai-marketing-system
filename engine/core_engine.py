from datetime import datetime

# =========================
# 🧠 CORE ENGINE V2
# =========================

def run_core_engine(products, metrics):
    """
    Zentrale AI Orchestrierung
    (Winner + Scaling + Decision Layer)
    """

    results = []

    for p in products:

        product_id = p.get("product_id", "UNKNOWN")
        score = p.get("score", 0)

        # 🧠 SIMPLE AI LOGIC (STABLE VERSION)
        if score >= 90:
            action = "SCALE_UP"
            multiplier = 2.0
        elif score >= 80:
            action = "SCALE"
            multiplier = 1.5
        else:
            action = "KEEP"
            multiplier = 1.0

        results.append({
            "product_id": product_id,
            "score": score,
            "action": action,
            "budget_multiplier": multiplier,
            "timestamp": datetime.now().isoformat()
        })

    return {
        "status": "CORE_ENGINE_ACTIVE",
        "results": results
    }
