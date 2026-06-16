from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.autopublish_engine import autopublish
from engine.pinterest_simulation_engine import simulate_pinterest_post
from engine.ads_budget_engine import decide_ads
from engine.scaling_engine import decide_scaling
from engine.dashboard_engine import build_dashboard, get_summary

from engine.tracking_engine import (
    log_event,
    get_product_stats,
    get_top_products
)

from engine.winner_detection_engine import detect_winners, decide_action

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

@app.route("/run")
def run():
    product = get_next_product()
    content = generate_content(product)

    log_event(product["product_id"], 10, 100, 0, "run")

    return jsonify({
        "status": "success",
        "product": product,
        "content": content
    })

@app.route("/autopilot")
def autopilot():
    product = get_next_product()

    metrics = {
        "hour": int(os.environ.get("HOUR", 10)),
        "clicks": 25,
        "sales": 1
    }

    autopublish_result = autopublish(product, metrics)
    ads_result = decide_ads(product, metrics["clicks"], metrics["sales"])
    scaling_result = decide_scaling(product, ads_result)

    log_event(product["product_id"], metrics["clicks"], 200, metrics["sales"], "autopilot")

    return jsonify({
        "status": "success",
        "autopublish": autopublish_result,
        "ads": ads_result,
        "scaling": scaling_result
    })

@app.route("/pinterest-test")
def pinterest_test():
    product = get_next_product()
    simulation = simulate_pinterest_post(product)

    log_event(
        product["product_id"],
        simulation["clicks"],
        simulation["impressions"],
        0,
        "pinterest"
    )

    return jsonify({
        "status": "success",
        "simulation": simulation
    })

@app.route("/winner-test")
def winner_test():
    products = [get_next_product() for _ in range(4)]

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

@app.route("/scaling-test")
def scaling_test():
    product = get_next_product()
    ads_result = decide_ads(product, clicks=30, sales=2)
    scaling_result = decide_scaling(product, ads_result)

    return jsonify({
        "status": "success",
        "product": product,
        "ads": ads_result,
        "scaling": scaling_result
    })

@app.route("/dashboard")
def dashboard():
    return jsonify(build_dashboard())

@app.route("/summary")
def summary():
    return jsonify(get_summary())

@app.route("/stats/<product_id>")
def stats(product_id):
    return jsonify(get_product_stats(product_id))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
