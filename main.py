from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "mode": "STABLE"
    })

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "product": {"product_id": "TEST_001", "score": 85},
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
        "autopublish": {"action": "PUBLISH_READY", "slot": "morning"},
        "ads": {"budget": 25, "level": "TEST"},
        "scaling": {"action": "TEST_MODE"}
    })

@app.route("/auto-loop")
def auto_loop():
    return jsonify({
        "status": "success",
        "message": "AUTO LOOP ACTIVE",
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

@app.route("/live-metrics")
def live_metrics():
    return jsonify({
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "mode": "AUTONOMOUS",
        "status": "READY"
    })

@app.route("/dashboard-monitor")
def dashboard_monitor():
    return jsonify({
        "status": "LIVE_DASHBOARD",
        "system": {
            "cloud_run": "ONLINE",
            "scheduler": "ACTIVE",
            "auto_loop": "ACTIVE"
        },
        "metrics": {
            "products_total": 45,
            "pins_total": 45,
            "blog_posts": 35,
            "landingpages": 35
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
