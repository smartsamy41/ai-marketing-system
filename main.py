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
        "auto_loop": "ACTIVE",
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE"
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
    return jsonify(get_sheet_metrics())

@app.route("/dashboard-monitor")
def dashboard_monitor():
    return jsonify(get_system_overview())

@app.route("/sheet-metrics")
def sheet_metrics():
    return jsonify(get_sheet_metrics())

@app.route("/partner-status")
def partner_status():
    return jsonify(get_partner_status())

@app.route("/data-overview")
def data_overview():
    return jsonify(get_system_overview())

def get_sheet_metrics():
    return {
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "clicks_total": 0,
        "conversions_total": 0,
        "earnings_total": 0,
        "source": "STATIC_READY_FOR_GOOGLE_SHEETS",
        "status": "READY"
    }

def get_partner_status():
    return {
        "amazon": "ACTIVE",
        "check24": "ACTIVE",
        "tarifcheck": "ACTIVE",
        "telekom": "PINS_YOUTUBE_ONLY",
        "pinterest": "STANDARD_ACCESS_PENDING",
        "blogger": "READY",
        "youtube": "READY"
    }

def get_system_overview():
    return {
        "metrics": get_sheet_metrics(),
        "partners": get_partner_status(),
        "status": "DATA_LAYER_READY"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
