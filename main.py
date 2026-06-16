from flask import Flask, jsonify
import os

from engine.core_engine import run_core_engine

app = Flask(__name__)

# =========================
# 🧠 TEST DATA LAYER
# =========================

def get_products():
    return [
        {"product_id": "AMZ_001", "score": 92, "source": "amazon"},
        {"product_id": "CHK24_001", "score": 85, "source": "check24"},
        {"product_id": "TC_001", "score": 78, "source": "tarifcheck"},
        {"product_id": "AMZ_002", "score": 91, "source": "amazon"},
        {"product_id": "CHK24_002", "score": 82, "source": "check24"}
    ]


def get_metrics():
    return {
        "clicks": 128,
        "conversions": 12,
        "revenue": 89.50,
        "cost": 45.00,
        "ctr": 3.42,
        "roi": 98.8
    }

# =========================
# 🚀 CORE ROUTES
# =========================

@app.route("/")
def home():
    return "AI MARKETING ENGINE V2 LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "version": "V2",
        "mode": "STABLE"
    })

@app.route("/run")
def run():

    products = get_products()
    metrics = get_metrics()

    result = run_core_engine(products, metrics)

    return jsonify({
        "status": "success",
        "mode": "V2_ENGINE",
        "input_metrics": metrics,
        "output": result
    })

@app.route("/metrics")
def metrics():
    return jsonify(get_metrics())

@app.route("/products")
def products():
    return jsonify(get_products())

@app.route("/system-status")
def system_status():
    return jsonify({
        "cloud_run": "ONLINE",
        "engine": "V2_ACTIVE",
        "core": "RUNNING",
        "scaling": "READY",
        "memory": "READY_FOR_NEXT_PHASE"
    })

# =========================
# ☁️ CLOUD RUN ENTRY POINT
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
