from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# CORE SYSTEM
# =========================

@app.route("/")
def home():
    return "AI Marketing System CORE LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "CORE_AI_MARKETING",
        "mode": "STABLE",
        "version": "CORE_RESET_V1"
    })

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "mode": "core",
        "product": {
            "product_id": "CORE_TEST",
            "score": 80
        },
        "pipeline": {
            "step_1": "product_selected",
            "step_2": "content_generated",
            "step_3": "ready_for_publishing"
        }
    })

@app.route("/autopilot")
def autopilot():
    return jsonify({
        "status": "success",
        "mode": "autopilot_core",
        "actions": [
            "select_product",
            "generate_content",
            "prepare_ads",
            "log_event"
        ],
        "budget": {
            "level": "SAFE_TEST",
            "amount": 10
        }
    })

# =========================
# SYSTEM INFO
# =========================

@app.route("/system")
def system():
    return jsonify({
        "name": "AI_MARKETING_SYSTEM",
        "architecture": "CORE_RESET",
        "status": "RUNNING",
        "timestamp": datetime.now().isoformat()
    })

# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
