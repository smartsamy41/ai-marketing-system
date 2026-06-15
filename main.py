from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.scheduler_engine import get_time_slot
from engine.learning_engine import update_score
from engine.autopublish_engine import autopublish
from engine.indexing_engine import submit_to_index

app = Flask(__name__)

# 🟢 HOME
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

# 🟢 TEST API
@app.route("/run")
def run():

    product = get_next_product()
    content = generate_content(product)

    return jsonify({
        "product": product,
        "content": content
    })

# 🟢 AUTOPILOT (STABLE VERSION)
@app.route("/autopilot")
def autopilot():

    product = get_next_product()

    metrics = {
        "hour": int(os.environ.get("HOUR", 10)),
        "clicks": 25,
        "sales": 1
    }

    # autopublish (includes logic + learning)
    result = autopublish(product, metrics)

    # indexing
    index_result = submit_to_index(
        f"https://your-domain.com/{product['product_id']}"
    )

    return jsonify({
        "status": "success",
        "autopublish": result,
        "indexing": index_result
    })


# 🟢 CLOUD RUN ENTRY POINT
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
