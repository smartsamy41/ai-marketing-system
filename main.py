from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.autopublish_engine import autopublish
from engine.pinterest_simulation_engine import simulate_pinterest_post
from engine.winner_detection_engine import detect_winners, decide_action

app = Flask(__name__)

# =========================
# 🟢 HOME
# =========================
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"


# =========================
# 🟢 RUN
# =========================
@app.route("/run")
def run():

    product = get_next_product()
    content = generate_content(product)

    return jsonify({
        "status": "success",
        "product": product,
        "content": content
    })


# =========================
# 🟢 AUTOPILOT
# =========================
@app.route("/autopilot")
def autopilot():

    product = get_next_product()

    metrics = {
        "hour": int(os.environ.get("HOUR", 10)),
        "clicks": 25,
        "sales": 1
    }

    result = autopublish(product, metrics)

    return jsonify({
        "status": "success",
        "autopublish": result
    })


# =========================
# 🟢 PINTEREST SIMULATION
# =========================
@app.route("/pinterest-test")
def pinterest_test():

    product = get_next_product()
    simulation = simulate_pinterest_post(product)

    return jsonify({
        "status": "success",
        "simulation": simulation
    })


# =========================
# 🟢 WINNER TEST (FIXED)
# =========================
@app.route("/winner-test")
def winner_test():

    products = [
        get_next_product(),
        get_next_product(),
        get_next_product(),
        get_next_product()
    ]

    winners = detect_winners(products)

    actions = []
    for p in products:
        actions.append({
            "product_id": p["product_id"],
            "score": p["score"],
            "action": decide_action(p)
        })

    return jsonify({
        "status": "success",
        "products": products,
        "winners": winners,
        "actions": actions
    })


# =========================
# 🟢 CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
