from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# 🟢 CORE ROUTES
# =========================

@app.route("/")
def home():
    return "AI MARKETING SYSTEM LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "mode": "STABLE"
    })

@app.route("/system-status")
def system_status():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "cloud_run": "ONLINE",
        "status": "HEALTHY"
    })

# =========================
# 🟢 DATA TEST ROUTES
# =========================

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "message": "ENGINE RUNNING",
        "data": {
            "product_id": "TEST_001",
            "score": 85
        }
    })

@app.route("/metrics")
def metrics():
    return jsonify({
        "products_total": 45,
        "pins_total": 45,
        "blog_posts": 35,
        "landingpages": 35,
        "status": "READY"
    })

@app.route("/events")
def events():
    return jsonify({
        "status": "CONNECTED",
        "events": [
            {"type": "click", "product": "AMZ_001"},
            {"type": "conversion", "product": "CHK24_001"}
        ]
    })

# =========================
# 🟢 SAFE ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
