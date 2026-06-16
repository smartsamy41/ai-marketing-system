from flask import Flask
import os
from datetime import datetime

from engine.output_lock import safe_json, lock_response

app = Flask(__name__)

# =========================
# CORE SAFE SYSTEM
# =========================

@app.route("/")
def home():
    return "AI MARKETING SYSTEM OUTPUT LOCK ACTIVE 🚀"

@app.route("/health")
@lock_response
def health():
    return {
        "system": "AI_MARKETING_ENGINE",
        "mode": "OUTPUT_LOCK_ACTIVE",
        "status": "STABLE"
    }

@app.route("/run")
@lock_response
def run():
    return {
        "product": {
            "id": "CORE_001",
            "score": 85
        },
        "pipeline": "SAFE_EXECUTION"
    }

@app.route("/autopilot")
@lock_response
def autopilot():
    return {
        "mode": "AUTOPILOT_LOCKED",
        "ads": "SAFE_MODE",
        "scaling": "CONTROLLED"
    }

@app.route("/system-status")
@lock_response
def system_status():
    return {
        "cloud_run": "ONLINE",
        "scheduler": "ACTIVE",
        "auto_loop": "ACTIVE",
        "output_lock": "ENABLED"
    }

# =========================
# CLOUD RUN ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
