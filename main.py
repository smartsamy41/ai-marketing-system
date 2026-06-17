from flask import Flask, jsonify, request
import os
import json
from datetime import datetime
import random

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# 💾 STORAGE
# =========================

MEMORY_FILE = "memory.json"
CLICK_FILE = "clicks.json"

def load_json(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w") as f:
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
        return [{"error": str(e)}]

# =========================
# 🧠 STEP C – PREDICTION
# =========================

def prediction_engine(products):
    results = []

    for p in products:

        base = p.get("score", 50)
        source = p.get("source", "")

        boost = 1.0

        if source == "amazon":
            boost += 0.4
        elif source == "check24":
            boost += 0.3
        elif source == "tarifcheck":
            boost += 0.35

        predicted = base * boost

        if predicted > 130:
            label = "HOT"
        elif predicted > 100:
            label = "GOOD"
        else:
            label = "NORMAL"

        results.append({
            "product": p,
            "predicted": round(predicted, 2),
            "label": label
        })

    return results

# =========================
# 🤖 STEP D – AUTOPILOT
# =========================

def autopilot(predictions):

    actions = []

    for p in predictions:

        label = p["label"]

        if label == "HOT":
            action = {"budget": 3.0, "decision": "SCALE_UP"}
        elif label == "GOOD":
            action = {"budget": 2.0, "decision": "BOOST"}
        else:
            action = {"budget": 1.0, "decision": "HOLD"}

        actions.append({
            "product": p["product"],
            "prediction": p,
            "action": action
        })

    return actions

# =========================
# 💰 STEP F – REAL WORLD ENGINE
# =========================

def real_world_engine(actions, clicks):

    enriched = []

    for a in actions:

        product_id = a["product"]["product_id"]

        product_clicks = [c for c in clicks if c["product_id"] == product_id]

        click_count = len(product_clicks)

        # 🔥 REAL WORLD SIGNAL SIMULATION
        traffic_score = click_count * random.uniform(0.8, 1.5)

        conversion = min(1.0, click_count / 15)

        revenue_score = traffic_score * conversion * a["action"]["budget"]

        if revenue_score > 25:
            decision = "INCREASE_BUDGET"
        elif revenue_score > 10:
            decision = "STABLE"
        else:
            decision = "CUT"

        enriched.append({
            "product_id": product_id,
            "clicks": click_count,
            "traffic_score": round(traffic_score, 2),
            "revenue_score": round(revenue_score, 2),
            "final_decision": decision,
            "budget": a["action"]["budget"]
        })

    return enriched

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP F REAL WORLD AI SYSTEM LIVE 🚀"

@app.route("/run")
def run():

    products = google_sheets_connect()
    predictions = prediction_engine(products)
    actions = autopilot(predictions)

    clicks = load_json(CLICK_FILE)

    result = real_world_engine(actions, clicks)

    return jsonify({
        "status": "success",
        "mode": "STEP_F_REAL_WORLD",
        "result": result
    })

# =========================
# 🔗 REAL AFFILIATE CLICK TRACKING
# =========================

@app.route("/click/<product_id>")
def click(product_id):

    clicks = load_json(CLICK_FILE)

    clicks.append({
        "product_id": product_id,
        "timestamp": datetime.now().isoformat()
    })

    save_json(CLICK_FILE, clicks)

    return jsonify({
        "status": "click_tracked",
        "product_id": product_id,
        "total_clicks": len(clicks)
    })

# =========================
# 📊 LIVE METRICS
# =========================

@app.route("/metrics")
def metrics():

    clicks = load_json(CLICK_FILE)

    return jsonify({
        "total_clicks": len(clicks),
        "system": "STEP_F_REAL_WORLD"
    })

# =========================
# 🧠 HEALTH
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_F"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
