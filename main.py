from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# 🟢 ROOT
# =========================

@app.route("/")
def home():
    return "AI MARKETING SYSTEM LIVE 🚀"

# =========================
# 🟢 HEALTH CHECK
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_SYSTEM",
        "mode": "SAFE_MODE",
        "timestamp": datetime.now().isoformat()
    })

# =========================
# 🟢 RUN (SAFE TEST ENGINE)
# =========================

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "mode": "SAFE_ENGINE",
        "result": {
            "product_id": "TEST_001",
            "score": 90,
            "action": "KEEP",
            "budget_multiplier": 1.0
        }
    })

# =========================
# 🟢 SYSTEM STATUS
# =========================

@app.route("/system-status")
def system_status():
    return jsonify({
        "cloud_run": "ONLINE",
        "engine": "SAFE_MODE_ACTIVE",
        "deployment": "STABLE",
        "learning": "DISABLED",
        "memory": "DISABLED"
    })

# =========================
# 🟢 BASIC METRICS
# =========================

@app.route("/metrics")
def metrics():
    return jsonify({
        "products_total": 45,
        "clicks": 120,
        "conversions": 8,
        "status": "STATIC_TEST_DATA"
    })

# =========================
# 🟢 ENTRY POINT
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
