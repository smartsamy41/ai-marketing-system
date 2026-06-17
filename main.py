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
CLICK_FILE = "clicks.json"

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

def load_clicks():
    if not os.path.exists(CLICK_FILE):
        return []
    try:
        with open(CLICK_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_clicks(data):
    with open(CLICK_FILE, "w") as f:
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
# 🧠 PREDICTION ENGINE (STEP C)
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
# 🚀 STEP D – AUTOPILOT
# =========================

def autopilot_engine(predictions):

    actions = []

    for pred in predictions:

        label = pred["label"]
        product = pred["product"]

        if label == "VERY_HIGH_WIN":
            decision = "SCALE_AGGRESSIVE"
            budget = 3.0
        elif label == "HIGH_WIN":
            decision = "SCALE_UP"
            budget = 2.0
        elif label == "MEDIUM":
            decision = "KEEP"
            budget = 1.5
        else:
            decision = "PAUSE"
            budget = 0.5

        actions.append({
            "product_id": product["product_id"],
            "decision": decision,
            "budget": budget,
            "timestamp": datetime.now().isoformat()
        })

    return actions

# =========================
# 💰 STEP E – REAL MONEY LOOP ENGINE
# =========================

def money_loop_engine(actions, clicks):

    enriched = []

    for action in actions:

        product_id = action["product_id"]

        # find clicks
        product_clicks = [c for c in clicks if c["product_id"] == product_id]

        click_count = len(product_clicks)
        conversion_rate = 0

        if click_count > 0:
            conversion_rate = min(1.0, click_count / 10)

        # ROI simulation
        roi_score = (action["budget"] * conversion_rate) * 10

        if roi_score > 20:
            money_action = "INCREASE_BUDGET"
        elif roi_score > 10:
            money_action = "STABLE"
        else:
            money_action = "CUT_BUDGET"

        enriched.append({
            "product_id": product_id,
            "action": action["decision"],
            "budget": action["budget"],
            "clicks": click_count,
            "conversion_rate": conversion_rate,
            "roi_score": roi_score,
            "money_action": money_action
        })

    return enriched

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP E MONEY LOOP ENGINE LIVE 🚀"

@app.route("/run")
def run():

    products = google_sheets_connect()

    predictions = prediction_engine(products)
    actions = autopilot_engine(predictions)

    clicks = load_clicks()

    money_loop = money_loop_engine(actions, clicks)

    return jsonify({
        "status": "success",
        "mode": "STEP_E_MONEY_LOOP",
        "predictions": predictions,
        "autopilot": actions,
        "money_loop": money_loop
    })

@app.route("/click")
def click_simulate():

    clicks = load_clicks()

    clicks.append({
        "product_id": "AMZ_001",
        "timestamp": datetime.now().isoformat()
    })

    save_clicks(clicks)

    return jsonify({
        "status": "click_saved",
        "total_clicks": len(clicks)
    })

@app.route("/metrics")
def metrics():

    clicks = load_clicks()

    return jsonify({
        "total_clicks": len(clicks),
        "system": "STEP_E_ACTIVE"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_E_MONEY_LOOP"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
