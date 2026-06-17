from flask import Flask, jsonify
import os
import json
from datetime import datetime
import random

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# 💾 STORAGE LAYER
# =========================

MEMORY_FILE = "memory.json"
CLICK_FILE = "clicks.json"
EVENTS_FILE = "events.json"

def load(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# 📊 GOOGLE SHEETS CONNECT
# =========================

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
RANGE = "products!A:C"

def sheets():
    try:
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ])

        service = build("sheets", "v4", credentials=creds)

        res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE
        ).execute()

        values = res.get("values", [])

        products = []

        for r in values[1:]:
            products.append({
                "id": r[0],
                "score": int(r[1]) if len(r) > 1 else 50,
                "source": r[2] if len(r) > 2 else "unknown"
            })

        return products

    except Exception as e:
        return [{"error": str(e)}]

# =========================
# 🧠 AI CORE (STEP C+D+E+F)
# =========================

def ai_engine(products, clicks):

    output = []

    for p in products:

        if "error" in p:
            continue

        base = p["score"]
        source = p["source"]

        # 🔥 Prediction Layer
        boost = {"amazon":1.4, "check24":1.3, "tarifcheck":1.35}.get(source, 1.0)
        predicted = base * boost

        # 🤖 Autopilot Decision
        if predicted > 130:
            decision = "AGGRESSIVE_SCALE"
            budget = 3.0
        elif predicted > 100:
            decision = "SCALE"
            budget = 2.0
        elif predicted > 80:
            decision = "STABLE"
            budget = 1.5
        else:
            decision = "CUT"
            budget = 0.5

        # 💰 Real World Feedback Loop
        product_clicks = [c for c in clicks if c["id"] == p["id"]]
        click_score = len(product_clicks)

        revenue = click_score * budget * random.uniform(0.8, 1.6)

        if revenue > 30:
            final_action = "SCALE_UP"
        elif revenue > 10:
            final_action = "HOLD"
        else:
            final_action = "REDUCE"

        output.append({
            "product": p,
            "predicted_score": round(predicted,2),
            "decision": decision,
            "budget": budget,
            "clicks": click_score,
            "revenue_score": round(revenue,2),
            "final_action": final_action
        })

    return output

# =========================
# 🚀 AUTONOMOUS BUSINESS LOOP
# =========================

@app.route("/")
def home():
    return "STEP G AUTONOMOUS AI BUSINESS ENGINE 🚀"

@app.route("/run")
def run():

    products = sheets()
    clicks = load(CLICK_FILE)

    result = ai_engine(products, clicks)

    # store event
    events = load(EVENTS_FILE)
    events.append({
        "time": datetime.now().isoformat(),
        "result_count": len(result)
    })
    save(EVENTS_FILE, events)

    return jsonify({
        "status": "success",
        "mode": "STEP_G_FULL_AUTONOMY",
        "results": result
    })

# =========================
# 🔗 REAL CLICK TRACKING
# =========================

@app.route("/click/<pid>")
def click(pid):

    clicks = load(CLICK_FILE)

    clicks.append({
        "id": pid,
        "time": datetime.now().isoformat()
    })

    save(CLICK_FILE, clicks)

    return jsonify({
        "status": "tracked",
        "product_id": pid,
        "total": len(clicks)
    })

# =========================
# 📊 METRICS
# =========================

@app.route("/metrics")
def metrics():

    return jsonify({
        "clicks": len(load(CLICK_FILE)),
        "events": len(load(EVENTS_FILE)),
        "system": "STEP_G"
    })

# =========================
# 🧠 HEALTH
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_G_FULL_AUTONOMY"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
