from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.autopublish_engine import autopublish
from engine.pinterest_simulation_engine import simulate_pinterest_post

# 🟢 TRACKING ENGINE (NEU KOMPLETT INTEGRIERT)
from engine.tracking_engine import (
    log_event,
    get_product_stats,
    get_top_products
)

app = Flask(__name__)

# =========================
# 🟢 HOME
# =========================
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"


# =========================
# 🟢 RUN (PRODUKT + CONTENT)
# =========================
@app.route("/run")
def run():

    product = get_next_product()
    content = generate_content(product)

    # 🟢 TRACKING EVENT (SIMULIERT ERSTE DATEN)
    log_event(
        product_id=product["product_id"],
        clicks=10,
        impressions=100,
        sales=0,
        platform="run"
    )

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

    # 🟢 TRACKING UPDATE
    log_event(
        product_id=product["product_id"],
        clicks=metrics["clicks"],
        impressions=200,
        sales=metrics["sales"],
        platform="autopilot"
    )

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

    # 🟢 TRACKING UPDATE
    log_event(
        product_id=product["product_id"],
        clicks=simulation["clicks"],
        impressions=simulation["impressions"],
        sales=0,
        platform="pinterest_sim"
    )

    return jsonify({
        "status": "success",
        "simulation": simulation
    })


# =========================
# 🟢 WINNER TEST
# =========================
@app.route("/winner-test")
def winner_test():

    products = [
        get_next_product(),
        get_next_product(),
        get_next_product(),
        get_next_product()
    ]

    return jsonify({
        "status": "success",
        "top_products": get_top_products(),
        "raw_products": products
    })


# =========================
# 🟢 PRODUCT STATS
# =========================
@app.route("/stats/<product_id>")
def stats(product_id):

    return jsonify(
        get_product_stats(product_id)
    )


# =========================
# 🟢 CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
