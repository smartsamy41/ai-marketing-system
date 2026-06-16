from flask import Flask, jsonify
import os
from datetime import datetime

from engine.data_layer_engine import (
    get_products,
    get_metrics,
    get_events,
    get_dashboard_data
)

app = Flask(__name__)

# =========================
# CORE
# =========================

@app.route("/")
def home():
    return "AI Marketing System DATA LAYER LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "mode": "DATA_LAYER_ACTIVE"
    })

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "product": {
            "product_id": "TEST_001",
            "score": 85
        },
        "content": {
            "blog": "Test Blog Content",
            "pin": "Test Pin",
            "youtube": "Test Video Script"
        }
    })

@app.route("/autopilot")
def autopilot():
    return jsonify({
        "status": "success",
        "autopublish": {
            "action": "PUBLISH_READY",
            "slot": "morning"
        },
        "ads": {
            "budget": 25,
            "level": "TEST"
        },
        "scaling": {
            "action": "TEST_MODE"
        }
    })

@app.route("/auto-loop")
def auto_loop():
    return jsonify({
        "status": "success",
        "auto_loop": "ACTIVE",
        "scheduler": "RUNNING"
    })

@app.route("/system-status")
def system_status():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "ACTIVE",
        "status": "HEALTHY"
    })

# =========================
# DATA LAYER API
# =========================

@app.route("/data/products")
def data_products():
    return jsonify(get_products())

@app.route("/data/metrics")
def data_metrics():
    return jsonify(get_metrics())

@app.route("/data/events")
def data_events():
    return jsonify(get_events())

@app.route("/data/dashboard")
def data_dashboard():
    return jsonify(get_dashboard_data())

# =========================
# LEGACY DASHBOARD (COMPAT)
# =========================

@app.route("/live-metrics")
def live_metrics():
    return jsonify(get_metrics())

@app.route("/dashboard-monitor")
def dashboard_monitor():
    return jsonify(get_dashboard_data())

# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
