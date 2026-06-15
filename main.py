from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content
from engine.scheduler_engine import get_time_slot
from engine.learning_engine import update_score
from engine.ai_decision_engine import choose_best
from engine.autopublish_engine import autopublish
from engine.indexing_engine import submit_to_index

app = Flask(__name__)

# 🟢 HOME
@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

# 🟢 BASIC RUN (OLD API)
@app.route("/run")
def run():

    product = get_next_product()
    content = generate_content(product)

    return jsonify({
        "product": product,
        "content": content
    })


# 🟢 FULL AUTOPILOT SYSTEM (PHASE 3)
@app.route("/autopilot")
def autopilot():

    product = get_next_product()

    # Simulated metrics (later real data)
    metrics = {
        "hour": int(os.environ.get("HOUR", 10)),
        "clicks": 25,
        "sales": 1
    }

    # AI Decision
    product = choose_best([product])

    # Autopublish logic
    result = autopublish(product, metrics)

    # Indexing (Google + Bing)
    index_result = submit_to_index(
        f"https://your-domain.com/{product['product_id']}"
    )

    return jsonify({
        "status": "success",
        "autopublish": result,
        "indexing": index_result
    })


# 🟢 ENTRY POINT (CLOUD RUN READY)
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
