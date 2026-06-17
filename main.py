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
# 📊 SHEETS CONNECT
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
# 💰 AFFILIATE SCORING
# =========================

def affiliate_score(product):
    score = product.get("score", 0)
    source = product.get("source", "unknown")

    multiplier = 1.0

    if source == "amazon":
        multiplier += 0.3
    elif source == "check24":
        multiplier += 0.2
    elif source == "tarifcheck":
        multiplier += 0.25

    return {
        "base_score": score,
        "multiplier": multiplier,
        "final_score": score * multiplier
    }

def budget_allocator(final_score):
    if final_score >= 120:
        return {"budget": 3.0, "level": "HIGH_SCALE"}
    elif final_score >= 90:
        return {"budget": 2.0, "level": "MID_SCALE"}
    elif final_score >= 70:
        return {"budget": 1.5, "level": "LOW_SCALE"}
    else:
        return {"budget": 1.0, "level": "HOLD"}

# =========================
# 🧠 STEP B MEMORY LEARNING (KEEP)
# =========================

def learning_engine(memory):
    stats = {}

    for entry in memory:
        pid = entry["product"]["product_id"]

        if pid not in stats:
            stats[pid] = {"win": 0, "loss": 0}

        if entry["budget"]["level"] == "HIGH_SCALE":
            stats[pid]["win"] += 1
        else:
            stats[pid]["loss"] += 1

    for entry in memory:
        pid = entry["product"]["product_id"]

        win = stats[pid]["win"]
        loss = stats[pid]["loss"]
        total = win + loss

        if total == 0:
            continue

        winrate = win / total

        # learning adjustment
        if winrate > 0.65:
            entry["product"]["score"] += 3
        elif winrate < 0.35:
            entry["product"]["score"] -= 3

    return memory

# =========================
# 🚀 STEP C – PREDICTION ENGINE
# =========================

def prediction_engine(products):
    predictions = []

    for p in products:

        score = p.get("score", 0)
        source = p.get("source", "unknown")

        multiplier = 1.0

        # trend boost simulation
        if source == "amazon":
            multiplier += 0.35
        elif source == "check24":
            multiplier += 0.25
        elif source == "tarifcheck":
            multiplier += 0.30

        predicted_score = score * multiplier

        # probability model (simple AI)
        if predicted_score >= 130:
            chance = "VERY_HIGH_WIN"
        elif predicted_score >= 100:
            chance = "HIGH_WIN"
        elif predicted_score >= 80:
            chance = "MEDIUM"
        else:
            chance = "LOW"

        predictions.append({
            "product": p,
            "predicted_score": round(predicted_score, 2),
            "prediction": chance
        })

    return predictions

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP C PREDICTION ENGINE LIVE 🚀"

@app.route("/run")
def run():

    products = google_sheets_connect()
    memory = load_memory()

    results = []

    for p in products:

        if "error" in p:
            continue

        score_data = affiliate_score(p)
        budget = budget_allocator(score_data["final_score"])

        entry = {
            "timestamp": datetime.now().isoformat(),
            "product": p,
            "score": score_data,
            "budget": budget
        }

        memory.append(entry)
        results.append(entry)

    # STEP B learning
    memory = learning_engine(memory)

    save_memory(memory)

    # STEP C prediction
    predictions = prediction_engine(products)

    return jsonify({
        "status": "success",
        "mode": "STEP_C_PREDICTION_ENGINE",
        "results": results,
        "predictions": predictions,
        "memory_size": len(memory)
    })

@app.route("/prediction")
def prediction():

    products = google_sheets_connect()
    return jsonify({
        "predictions": prediction_engine(products)
    })

@app.route("/memory")
def memory():
    return jsonify({
        "memory_size": len(load_memory()),
        "data": load_memory()
    })

@app.route("/data-source")
def data_source():
    return jsonify({
        "source": "GOOGLE_SHEETS_REAL",
        "data": google_sheets_connect()
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_C"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
