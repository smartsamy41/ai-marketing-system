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
from engine.scaling_engine import decide_scaling

# 🟢 AUTO LOOP IMPORT
from engine.auto_loop_engine import run_auto_loop

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

    log_event(product["product_id"], 10, 100, 0, "run")

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
        "clicks": 25,
        "sales": 1
    }

    publish = autopublish(product, metrics)
    ads = decide_ads(product, metrics["clicks"], metrics["sales"])
    scaling = decide_scaling(product, ads)

    log_event(product["product_id"], metrics["clicks"], 200, metrics["sales"], "autopilot")

    return jsonify({
        "status": "success",
        "autopublish": publish,
        "ads": ads,
        "scaling": scaling
    })


# =========================
# 🟢 PINTEREST SIM
# =========================
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


# =========================
# 🟢 WINNER SYSTEM
# =========================
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


# =========================
# 🟢 AUTO LOOP (NEU)
# =========================
@app.route("/auto-loop")
def auto_loop():

    result = run_auto_loop(iterations=5, sleep_time=1)

    return jsonify(result)


# =========================
# 🟢 STATS
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
