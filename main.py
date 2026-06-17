from flask import Flask, jsonify
import os
import json
from datetime import datetime

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# 💾 MEMORY SYSTEM
# =========================

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# 📊 GOOGLE SHEETS CONNECT
# =========================

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
RANGE_NAME = "products!A:C"

def google_sheets_connect():
    try:
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ])

        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get("values", [])

        products = []

        for row in values[1:]:
            product_id = row[0] if len(row) > 0 else "unknown"

            try:
                score = int(row[1])
            except:
                score = 50

            source = row[2] if len(row) > 2 else "unknown"

            products.append({
                "product_id": product_id,
                "score": score,
                "source": source
            })

        return products

    except Exception as e:
        return [{"error": str(e), "source": "sheets_failed"}]

# =========================
# 🧠 STEP C – PREDICTION ENGINE
# =========================

def prediction_engine(products):
    predictions = []

    for p in products:

        score = p.get("score", 0)
        source = p.get("source", "unknown")

        boost = 1.0

        if source == "amazon":
            boost += 0.35
        elif source == "check24":
            boost += 0.25
        elif source == "tarifcheck":
            boost += 0.30

        predicted = score * boost

        if predicted >= 130:
            label = "VERY_HIGH_WIN"
        elif predicted >= 100:
            label = "HIGH_WIN"
        elif predicted >= 80:
            label = "MEDIUM"
        else:
            label = "LOW"

        predictions.append({
            "product": p,
            "predicted_score": round(predicted, 2),
            "label": label
        })

    return predictions

# =========================
# 🚀 STEP D – AUTOPILOT ENGINE
# =========================

def autopilot_engine(products, predictions):

    actions = []

    for pred in predictions:

        product = pred["product"]
        label = pred["label"]

        action = {
            "product_id": product["product_id"],
            "decision": None,
            "budget_action": None
        }

        # 🔥 AUTOPILOT DECISION LOGIC

        if label == "VERY_HIGH_WIN":
            action["decision"] = "AUTO_SCALE_UP"
            action["budget_action"] = 3.0

        elif label == "HIGH_WIN":
            action["decision"] = "SCALE_UP"
            action["budget_action"] = 2.0

        elif label == "MEDIUM":
            action["decision"] = "KEEP"
            action["budget_action"] = 1.5

        else:
            action["decision"] = "PAUSE"
            action["budget_action"] = 0.5

        actions.append(action)

    return actions

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP D AUTOPILOT ENGINE LIVE 🚀"

@app.route("/run")
def run():

    products = google_sheets_connect()

    # STEP C
    predictions = prediction_engine(products)

    # STEP D
    actions = autopilot_engine(products, predictions)

    return jsonify({
        "status": "success",
        "mode": "STEP_D_AUTOPILOT",
        "predictions": predictions,
        "autopilot_actions": actions
    })

@app.route("/prediction")
def prediction():
    products = google_sheets_connect()
    return jsonify(prediction_engine(products))

@app.route("/autopilot")
def autopilot():
    products = google_sheets_connect()
    predictions = prediction_engine(products)
    return jsonify(autopilot_engine(products, predictions))

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_D_AUTOPILOT"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
