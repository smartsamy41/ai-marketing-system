from flask import Flask
import os
from datetime import datetime

from engine.output_lock import success, system_response
from engine.winner_engine import decide_action
from engine.scaling_engine import calculate_scaling
from engine.data_connect import get_live_events, get_live_metrics, get_product_feed

app = Flask(__name__)

# =========================
# CORE
# =========================

@app.route("/")
def home():
    return "AI MARKETING DATA CONNECT LIVE 🚀"

@app.route("/health")
def health():
    return system_response("DATA_CONNECT_ENGINE", {
        "status": "STABLE",
        "mode": "LIVE_DATA_ACTIVE"
    })

@app.route("/run")
def run():

    products = get_product_feed()
    metrics = get_live_metrics()

    results = []

    for p in products:
        results.append({
            "product": p,
            "winner": decide_action(p),
            "scaling": calculate_scaling(p, metrics)
        })

    return success({
        "mode": "DATA_CONNECTED",
        "results": results
    })

@app.route("/events")
def events():
    return success({
        "events": get_live_events(),
        "status": "CONNECTED"
    })

@app.route("/metrics")
def metrics():
    return success(get_live_metrics())

@app.route("/products")
def products():
    return success(get_product_feed())

@app.route("/system-status")
def system_status():
    return success({
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "ACTIVE",
        "data_connect": "ENABLED"
    })

# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
