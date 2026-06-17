from flask import Flask, jsonify
from app.core_engine import run_engine

app = Flask(__name__)

# =========================
# HEALTH
# =========================

@app.route("/")
def home():
    return "MASTER AI ENGINE LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({"status": "OK", "engine": "MASTER_V1"})

# =========================
# RUN ENGINE
# =========================

@app.route("/run")
def run():
    try:
        data = run_engine()
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
# DEBUG
# =========================

@app.route("/debug")
def debug():
    return jsonify({
        "status": "debug_active",
        "engine": "MASTER_CONTROL_FLOW"
    })

# =========================
# START
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
