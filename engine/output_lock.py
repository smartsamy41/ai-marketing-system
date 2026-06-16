from flask import jsonify
from datetime import datetime

# =========================
# OUTPUT LOCK SYSTEM FIXED
# =========================

def success(data):
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": data
    })


def error(message):
    return jsonify({
        "status": "error",
        "timestamp": datetime.now().isoformat(),
        "message": message
    })


def system_response(system, state):
    return jsonify({
        "status": "success",
        "system": system,
        "timestamp": datetime.now().isoformat(),
        "state": state
    })
