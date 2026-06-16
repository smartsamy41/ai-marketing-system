from flask import Flask
import os

from engine.output_lock import success, system_response
from engine.winner_engine import decide_action
from engine.scaling_engine import calculate_scaling
from engine.data_connect import get_product_feed, get_live_metrics
from engine.learning_layer import log_decision, analyze_learning
from engine.memory_layer import store_event, get_memory, analyze_memory

app = Flask(__name__)

# =========================
# CORE
# =========================

@app.route("/")
def home():
    return "AI MEMORY LAYER ENGINE LIVE 🚀"


@app.route("/run")
def run():

    products = get_product_feed()
    metrics = get_live_metrics()

    results = []

    for p in products:

        winner = decide_action(p)
        scaling = calculate_scaling(p, metrics)

        # 🧠 LEARNING
        learning = log_decision(p, winner, scaling)

        # 🧠 MEMORY STORE (NEU)
        store_event("decision", {
            "product": p,
            "winner": winner,
            "scaling": scaling
        })

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling,
            "learning": learning
        })

    return success({
        "mode": "FULL_MEMORY_ACTIVE",
        "results": results
    })


# -------------------------
# MEMORY ENDPOINTS
# -------------------------

@app.route("/memory")
def memory():
    return success(get_memory())


@app.route("/memory/insights")
def memory_insights():
    return success(analyze_memory())


@app.route("/learning")
def learning():
    return success(analyze_learning())


@app.route("/system-status")
def system_status():
    return success({
        "cloud_run": "ONLINE",
        "data_connect": "ACTIVE",
        "learning_layer": "ACTIVE",
        "memory_layer": "ENABLED",
        "autonomous_mode": "TRUE"
    })


# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
