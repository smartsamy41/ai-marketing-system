import json
from flask import jsonify
from datetime import datetime

# =========================
# 🔒 OUTPUT LOCK SYSTEM
# =========================

def safe_json(data):
    """
    Erzwingt sauberes JSON Output
    verhindert String-Konkatenation Fehler
    """

    try:
        # Validierung → darf kein String sein
        if isinstance(data, str):
            return jsonify({
                "status": "error",
                "error": "INVALID_STRING_RESPONSE_BLOCKED",
                "timestamp": datetime.now().isoformat()
            })

        # JSON-safe check
        json.dumps(data)

        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })


def lock_response(func):
    """
    Decorator: erzwingt saubere API Responses
    """

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return safe_json(result)

    wrapper.__name__ = func.__name__
    return wrapper
