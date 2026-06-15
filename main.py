from flask import Flask, jsonify
import os

from engine.decision_engine import get_next_product
from engine.content_engine import generate_content

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Marketing System LIVE 🚀"

@app.route("/run")
def run():
    product = get_next_product()
    content = generate_content(product)

    return jsonify({
        "product": product,
        "content": content
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
