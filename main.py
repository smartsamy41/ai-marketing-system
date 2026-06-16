from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.scheduler_engine import get_time_slot
from engine.learning_engine import update_score
from engine.autopublish_engine import autopublish

# 🟢 Pinterest Simulation Engine
from engine.pinterest_simulation_engine import simulate_pinterest_post

app = Flask(__name__)

# =========================
# 🟢 HOME
# =========================
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

# =========================
# 🟢 RUN (TEST PRODUCT FLOW)
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
# 🟢 AUTOPILOT (LIVE LOGIC)
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
# 🟢 PINTEREST SIMULATION TEST
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
# 🟢 CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
