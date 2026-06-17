from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# 🧠 MEMORY (IN RAM)
# =========================

MEMORY = []

# =========================
# 🧠 TEST DATA
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
    score = product["score"]

    if score >= 90:
        return {"action": "WINNER", "weight": 3}
    elif score >= 80:
        return {"action": "KEEP", "weight": 2}
    else:
        return {"action": "LOW", "weight": 1}

# =========================
# 📈 SCALING ENGINE
# =========================

def calculate_scaling(product):
    score = product["score"]

    if score >= 90:
        return {"budget": 2.0}
    elif score >= 80:
        return {"budget": 1.5}
    else:
        return {"budget": 1.0}

# =========================
# 🧠 LEARNING ENGINE (NEW)
# =========================

def learning_engine(memory):
    """
    Simple learning:
    - boost score if WINNER
    - reduce score if LOW
    """

    for entry in memory:

        if entry["winner"]["action"] == "WINNER":
            entry["product"]["score"] += 1

        if entry["winner"]["action"] == "LOW":
            entry["product"]["score"] -= 1

    return memory

# =========================
# 💾 SAVE MEMORY
# =========================

def save_memory(product, winner, scaling):

    entry = {
        "timestamp": datetime.now().isoformat(),
        "product": product,
        "winner": winner,
        "scaling": scaling
    }

    MEMORY.append(entry)

    return entry

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "AI ENGINE STEP 3 LEARNING ACTIVE 🚀"

@app.route("/run")
def run():

    products = get_products()

    results = []

    for p in products:

        winner = decide_winner(p)
        scaling = calculate_scaling(p)

        save_memory(p, winner, scaling)

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling
        })

    # 🧠 APPLY LEARNING AFTER RUN
    learned = learning_engine(MEMORY)

    return jsonify({
        "status": "success",
        "mode": "STEP_3_LEARNING",
        "results": results,
        "learned_memory": learned
    })

@app.route("/memory")
def memory():
    return jsonify({
        "size": len(MEMORY),
        "data": MEMORY
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP3"
    })

@app.route("/system-status")
def status():
    return jsonify({
        "engine": "STEP3_LEARNING_ACTIVE",
        "memory": len(MEMORY),
        "learning": "ON",
        "status": "STABLE"
    })

# =========================
# ☁️ ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
