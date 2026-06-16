from flask import Flask, jsonify
import os

from engine.dashboard_monitoring_engine import (
    get_dashboard,
    get_system_status,
    get_live_metrics
)

app = Flask(__name__)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"


# =========================
# HEALTH
# =========================
@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "mode": "STABLE"
    })


# =========================
# RUN
# =========================
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


# =========================
# AUTOPILOT
# =========================
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


# =========================
# AUTO LOOP
# =========================
@app.route("/auto-loop")
def auto_loop():

    return jsonify({
        "status": "success",
        "message": "AUTO LOOP ACTIVE",
        "scheduler": "RUNNING"
    })


# =========================
# SYSTEM STATUS
# =========================
@app.route("/system-status")
def system_status():

    return jsonify(get_system_status())


# =========================
# LIVE METRICS
# =========================
@app.route("/live-metrics")
def live_metrics():

    return jsonify(get_live_metrics())


# =========================
# DASHBOARD MONITOR
# =========================
@app.route("/dashboard-monitor")
def dashboard_monitor():

    return jsonify(get_dashboard())


# =========================
# CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
