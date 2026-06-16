from flask import Flask, jsonify
import os

app = Flask(__name__)

# =========================
# 🟢 HOME (MUSS IMMER GEHEN)
# =========================
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"


# =========================
# 🟢 HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "system": "AI_MARKETING_ENGINE",
        "mode": "STABLE"
    })


# =========================
# 🟢 RUN (SAFE MOCK)
# =========================
@app.route("/run")
def run():

    return jsonify({
        "status": "success",
        "product": {
            "product_id": "TEST_001",
            "score": 85
        },
        "content": {
            "blog": "Test Blog Content",
            "pin": "Test Pin",
            "youtube": "Test Video Script"
        }
    })


# =========================
# 🟢 AUTOPILOT (SAFE MOCK)
# =========================
@app.route("/autopilot")
def autopilot():

    return jsonify({
        "status": "success",
        "autopublish": {
            "action": "PUBLISH_READY",
            "slot": "morning"
        },
        "ads": {
            "budget": 25,
            "level": "TEST"
        },
        "scaling": {
            "action": "TEST_MODE"
        }
    })


# =========================
# 🟢 PINTEREST SIMULATION
# =========================
@app.route("/pinterest-test")
def pinterest_test():

    return jsonify({
        "status": "success",
        "simulation": {
            "product_id": "TEST_001",
            "clicks": 50,
            "impressions": 1000,
            "ctr": 5.0
        }
    })


# =========================
# 🟢 WINNER TEST
# =========================
@app.route("/winner-test")
def winner_test():

    return jsonify({
        "status": "success",
        "winners": [
            {"product_id": "TEST_001", "score": 90},
            {"product_id": "TEST_002", "score": 85}
        ],
        "actions": [
            {"product_id": "TEST_001", "action": "SCALE"},
            {"product_id": "TEST_002", "action": "TEST"}
        ]
    })


# =========================
# 🟢 AUTO LOOP SAFE (NO CRASH)
# =========================
@app.route("/auto-loop")
def auto_loop():

    return jsonify({
        "status": "success",
        "message": "AUTO LOOP SAFE MODE ACTIVE",
        "iterations": 3,
        "note": "Engine isolated for stability"
    })


# =========================
# 🟢 STATS
# =========================
@app.route("/stats/<product_id>")
def stats(product_id):

    return jsonify({
        "product_id": product_id,
        "clicks": 120,
        "impressions": 3000,
        "sales": 5,
        "ctr": 4.0
    })


# =========================
# 🟢 CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
