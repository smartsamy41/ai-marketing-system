from flask import Flask, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# =========================
# 💾 PERSISTENT MEMORY FILE
# =========================

MEMORY_FILE = "memory.json"

# =========================
# 🧠 LOAD MEMORY
# =========================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

# =========================
# 💾 SAVE MEMORY
# =========================

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

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
# 🧠 LEARNING ENGINE
# =========================

def learning_engine(memory):

    for entry in memory:

        if entry["winner"]["action"] == "WINNER":
            entry["product"]["score"] += 1

        elif entry["winner"]["action"] == "LOW":
            entry["product"]["score"] -= 1

    return memory

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "AI ENGINE STEP 4 PERSISTENT MEMORY ACTIVE 🚀"

@app.route("/run")
def run():

    memory = load_memory()

    products = get_products()

    results = []

    for p in products:

        winner = decide_winner(p)
        scaling = calculate_scaling(p)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "product": p,
            "winner": winner,
            "scaling": scaling
        }

        memory.append(entry)

        results.append(entry)

    # 🧠 APPLY LEARNING
    memory = learning_engine(memory)

    # 💾 SAVE TO FILE (PERSISTENT)
    save_memory(memory)

    return jsonify({
        "status": "success",
        "mode": "STEP_4_PERSISTENT_MEMORY",
        "results": results,
        "memory_size": len(memory)
    })

@app.route("/memory")
def memory():

    memory = load_memory()

    return jsonify({
        "status": "OK",
        "memory_size": len(memory),
        "data": memory
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP4",
        "memory": "PERSISTENT"
    })

@app.route("/system-status")
def status():
    return jsonify({
        "engine": "STEP4_PERSISTENT_MEMORY",
        "status": "STABLE",
        "learning": "ON",
        "memory": "FILE_BASED"
    })

# =========================
# ☁️ ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
