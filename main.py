from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.autopublish_engine import autopublish
from engine.pinterest_simulation_engine import simulate_pinterest_post

from engine.tracking_engine import (
    log_event,
    get_product_stats,
    get_top_products
)

from engine.winner_detection_engine import detect_winners, decide_action

from engine.ads_budget_engine import decide_ads

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
# 🟢 AUTOPILOT (JETZT MIT ADS LOGIC)
# =========================
@app.route("/autopilot")
def autopilot():

    product = get_next_product()

    metrics = {
        "hour": int(os.environ.get("HOUR", 10)),
        "clicks": 25,
        "sales": 1
    }

    autopublish_result = autopublish(product, metrics)

    ads_result = decide_ads(
        product,
        clicks=metrics["clicks"],
        sales=metrics["sales"]
    )

    log_event(
        product_id=product["product_id"],
        clicks=metrics["clicks"],
        impressions=200,
        sales=metrics["sales"],
        platform="autopilot"
    )

    return jsonify({
        "status": "success",
        "autopublish": autopublish_result,
        "ads": ads_result
    })


# =========================
# 🟢 PINTEREST SIMULATION
# =========================
@app.route("/pinterest-test")
def pinterest_test():

    product = get_next_product()
    simulation = simulate_pinterest_post(product)

    log_event(
        product_id=product["product_id"],
        clicks=simulation["clicks"],
        impressions=simulation["impressions"],
        sales=0,
        platform="pinterest"
    )

    return jsonify({
        "status": "success",
        "simulation": simulation
    })


# =========================
# 🟢 WINNER SYSTEM
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
        "winners": detect_winners(products),
        "actions": [
            {
                "product_id": p["product_id"],
                "score": p["score"],
                "action": decide_action(p)
            }
            for p in products
        ],
        "top_products": get_top_products()
    })


# =========================
# 🟢 PRODUCT STATS
# =========================
@app.route("/stats/<product_id>")
def stats(product_id):

    return jsonify(get_product_stats(product_id))


# =========================
# 🟢 CLOUD RUN ENTRY
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
