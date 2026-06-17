from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# 🧠 MEMORY STORE (IN-MEMORY)
# =========================

MEMORY_LOG = []


# =========================
# 🧠 TEST PRODUCTS
# =========================

def get_products():
    return [
        {"product_id": "AMZ_001", "score": 92},
        {"product_id": "CHK24_001", "score": 85},
        {"product_id": "TC_001", "score": 78}
    ]


# =========================
# 🧠 WINNER ENGINE
# =========================

def decide_winner(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"action": "WINNER", "reason": "HIGH_SCORE"}
    elif score >= 80:
        return {"action": "KEEP", "reason": "STABLE"}
    else:
        return {"action": "LOW", "reason": "WEAK"}


# =========================
# 📈 SCALING ENGINE
# =========================

def calculate_scaling(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"budget_multiplier": 2.0, "action": "AGGRESSIVE_SCALE"}
    elif score >= 80:
        return {"budget_multiplier": 1.5, "action": "NORMAL_SCALE"}
    else:
        return {"budget_multiplier": 1.0, "action": "NO_SCALE"}


# =========================
# 🧠 MEMORY SAVE FUNCTION
# =========================

def save_to_memory(product, winner, scaling):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "product": product,
        "winner": winner,
        "scaling": scaling
    }

    MEMORY_LOG.append(entry)

    return entry


# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "AI ENGINE STEP 2 MEMORY LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP2",
        "memory": "ACTIVE"
    })


@app.route("/run")
def run():

    products = get_products()

    results = []

    for p in products:

        winner = decide_winner(p)
        scaling = calculate_scaling(p)

        memory = save_to_memory(p, winner, scaling)

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling,
            "memory_saved": True
        })

    return jsonify({
        "status": "success",
        "mode": "STEP_2_MEMORY_ACTIVE",
        "results": results
    })


@app.route("/memory")
def memory():

    return jsonify({
        "status": "OK",
        "memory_size": len(MEMORY_LOG),
        "data": MEMORY_LOG
    })


@app.route("/system-status")
def system_status():
    return jsonify({
        "cloud_run": "ONLINE",
        "engine": "STEP2_MEMORY_ACTIVE",
        "memory_entries": len(MEMORY_LOG),
        "status": "STABLE"
    })


# =========================
# ☁️ ENTRY POINT
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
