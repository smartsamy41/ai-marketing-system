from flask import Flask, jsonify

from engine.auto_loop_engine import run_autopilot
from engine.scheduler_engine import run_scheduler
from engine.data_layer_engine import load_products
from engine.tracking_engine import get_top_products
from engine.learning_engine import get_learning_summary

app = Flask(__name__)

# =========================
# 🟢 HOME
# =========================

@app.route("/")
def home():
    return "MASTER AI AFFILIATE ENGINE LIVE 🚀"


# =========================
# 🟢 HEALTH CHECK
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "engine": "AUTOPILOT_V1",
        "system": "RUNNING"
    })


# =========================
# 🚀 FULL AUTOPILOT RUN
# =========================

@app.route("/run")
def run():
    try:
        data = run_autopilot()

        return jsonify({
            "status": "success",
            "mode": "AUTOPILOT",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================
# ⏰ SCHEDULER ONLY TEST
# =========================

@app.route("/schedule")
def schedule():
    try:
        products = load_products()
        data = run_scheduler(products)

        return jsonify({
            "status": "success",
            "mode": "SCHEDULER_ONLY",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================
# 📊 TOP PRODUCTS
# =========================

@app.route("/top")
def top():
    try:
        data = get_top_products()

        return jsonify({
            "status": "success",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================
# 🧠 LEARNING SUMMARY
# =========================

@app.route("/learning")
def learning():
    try:
        data = get_learning_summary()

        return jsonify({
            "status": "success",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
