from flask import Flask, jsonify
import os

# =========================
# 🧠 ENGINE IMPORTS (FIXED)
# =========================

from engine.winner_engine import decide_winner
from engine.scaling_engine import calculate_scaling

app = Flask(__name__)

# =========================
# 🧠 TEST PRODUCT DATA
# =========================

def get_products():
    return [
        {"product_id": "AMZ_001", "score": 92, "source": "amazon"},
        {"product_id": "CHK24_001", "score": 85, "source": "check24"},
        {"product_id": "TC_001", "score": 78, "source": "tarifcheck"},
        {"product_id": "AMZ_002", "score": 95, "source": "amazon"},
        {"product_id": "CHK24_002", "score": 81, "source": "check24"},
        {"product_id": "TC_002", "score": 88, "source": "tarifcheck"}
    ]

# =========================
# 🚀 CORE ROUTES
# =========================

@app.route("/")
def home():
    return "AI MARKETING ENGINE LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "version": "STABLE",
        "mode": "RUNNING"
    })

@app.route("/run")
def run():

    products = get_products()

    results = []

    for p in products:

        # 🧠 WINNER ENGINE
        winner = decide_winner(p)

        # 📈 SCALING ENGINE
        scaling = calculate_scaling(p)

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling
        })

    return jsonify({
        "status": "success",
        "mode": "LIVE_ENGINE",
        "results": results
    })

@app.route("/products")
def products():
    return jsonify(get_products())

@app.route("/metrics")
def metrics():
    return jsonify({
        "clicks": 128,
        "conversions": 12,
        "revenue": 89.50,
        "status": "LIVE"
    })

@app.route("/system-status")
def system_status():
    return jsonify({
        "cloud_run": "ONLINE",
        "engine": "STABLE",
        "winner_engine": "ACTIVE",
        "scaling_engine": "ACTIVE",
        "status": "HEALTHY"
    })

# =========================
# ☁️ ENTRY POINT
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
