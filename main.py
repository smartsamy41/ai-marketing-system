from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.scheduler_engine import get_time_slot
from engine.learning_engine import update_score
from engine.autopublish_engine import autopublish

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

@app.route("/run")
def run():
    product = get_next_product()
    content = generate_content(product)

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

    result = autopublish(product, metrics)

    return jsonify({
        "status": "success",
        "autopublish": result
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
