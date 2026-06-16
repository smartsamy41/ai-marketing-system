from flask import Flask
import os

from engine.output_lock import success, system_response
from engine.winner_engine import decide_action
from engine.scaling_engine import calculate_scaling
from engine.data_connect import get_product_feed, get_live_metrics
from engine.learning_layer import log_decision, get_learning_data, analyze_learning

app = Flask(__name__)

# =========================
# CORE ENGINE
# =========================

@app.route("/")
def home():
    return "AI MARKETING LEARNING ENGINE LIVE 🚀"

@app.route("/run")
def run():

    products = get_product_feed()
    metrics = get_live_metrics()

    results = []

    for p in products:

        winner = decide_action(p)
        scaling = calculate_scaling(p, metrics)

        # 🧠 LEARNING LOG
        learning = log_decision(p, winner, scaling)

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling,
            "learning_log": learning
        })

    return success({
        "mode": "LEARNING_ACTIVE",
        "results": results
    })


@app.route("/learning")
def learning():
    return success(get_learning_data())


@app.route("/insights")
def insights():
    return success(analyze_learning())


@app.route("/system-status")
def system_status():
    return success({
        "cloud_run": "ONLINE",
        "auto_loop": "ACTIVE",
        "data_connect": "ACTIVE",
        "learning_layer": "ENABLED"
    })


# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
