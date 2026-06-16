from flask import jsonify
from datetime import datetime

# =========================
# 🟢 SAFE RESPONSE WRAPPER
# =========================

def success(data: dict):
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": data
    })


def error(message: str):
    return jsonify({
        "status": "error",
        "timestamp": datetime.now().isoformat(),
        "message": message
    })


def system_response(system: str, state: dict):
    return jsonify({
        "status": "success",
        "system": system,
        "timestamp": datetime.now().isoformat(),
        "state": state
    })
