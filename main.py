from flask import Flask, jsonify
import os
from datetime import datetime

from engine.winner_engine import detect_winners, decide_action

app = Flask(__name__)

# =========================
# CORE
# =========================

@app.route("/")
def home():
    return "AI Marketing System WINNER ENGINE LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "WINNER_AI_ENGINE",
        "mode": "STABLE"
    })

@app.route("/run")
def run():

    product = {
        "product_id": "TEST_001",
        "score": 88
    }

    return jsonify({
        "status": "success",
        "product": product,
        "decision": decide_action(product)
    })

@app.route("/winner-test")
def winner_test():

    products = [
        {"product_id": "A1", "score": 95},
        {"product_id": "A2", "score": 82},
        {"product_id": "A3", "score": 76},
        {"product_id": "A4", "score": 60}
    ]

    return jsonify({
        "status": "success",
        "winners": detect_winners(products),
        "decisions": [decide_action(p) for p in products]
    })

@app.route("/auto-loop")
def auto_loop():
    return jsonify({
        "status": "success",
        "mode": "WINNER_LOOP_ACTIVE",
        "scheduler": "RUNNING"
    })

@app.route("/system-status")
def system_status():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "system": "WINNER_ENGINE",
        "cloud_run": "ONLINE",
        "status": "HEALTHY"
    })

# =========================
# CLOUD RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
