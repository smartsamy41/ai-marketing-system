from flask import Flask
import os
from datetime import datetime

from engine.output_lock import success, system_response
from engine.winner_engine import decide_action
from engine.scaling_engine import calculate_scaling  # EXISTIERT BEREITS → KEIN DUPLIKAT

app = Flask(__name__)

# =========================
# CORE
# =========================

@app.route("/")
def home():
    return "AI MARKETING SYSTEM SCALING ENGINE LIVE 🚀"

@app.route("/health")
def health():
    return system_response("AI_SCALING_ENGINE", {
        "status": "STABLE",
        "mode": "SCALING_ACTIVE"
    })

@app.route("/run")
def run():

    product = {
        "product_id": "TEST_001",
        "score": 88
    }

    metrics = {
        "clicks": 15,
        "sales": 1
    }

    winner = decide_action(product)
    scaling = calculate_scaling(product, metrics)

    return success({
        "product": product,
        "winner_decision": winner,
        "scaling_decision": scaling
    })

@app.route("/autopilot")
def autopilot():
    return success({
        "mode": "AUTOPILOT_SCALING",
        "system": "ACTIVE",
        "actions": [
            "detect_winner",
            "calculate_scaling",
            "adjust_budget"
        ]
    })

@app.route("/system-status")
def system_status():
    return success({
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "ACTIVE",
        "scaling_engine": "ENABLED"
    })

# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
