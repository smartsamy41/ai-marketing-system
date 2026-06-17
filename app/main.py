from flask import Flask, jsonify
from engine.core_engine import run_engine
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "MASTER AI ENGINE LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "engine": "MASTER_V1"
    })

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

@app.route("/debug")
def debug():
    return jsonify({
        "status": "debug_active",
        "engine": "MASTER_CONTROL_FLOW"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
