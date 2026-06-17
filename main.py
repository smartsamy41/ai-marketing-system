from flask import Flask, jsonify
import os
import json
from datetime import datetime
import hashlib

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# 💾 STORAGE
# =========================

MEMORY_FILE = "memory.json"
CLICK_FILE = "clicks.json"
TRACK_FILE = "tracking.json"

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
# 📊 SHEETS CONNECT
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

        return [
            {
                "id": r[0],
                "score": int(r[1]) if len(r) > 1 else 50,
                "source": r[2] if len(r) > 2 else "unknown"
            }
            for r in values[1:]
        ]

    except Exception as e:
        return [{"error": str(e)}]

# =========================
# 🔥 STEP H – TRACKING ENGINE
# =========================

def generate_tracking_link(product_id, source):

    base_url = {
        "amazon": "https://amazon.com/dp/",
        "check24": "https://check24.de/product/",
        "tarifcheck": "https://tarifcheck.de/product/"
    }.get(source, "https://example.com/product/")

    raw = f"{product_id}-{datetime.now().isoformat()}"

    tracking_id = hashlib.md5(raw.encode()).hexdigest()[:10]

    full_url = f"{base_url}{product_id}?ref={tracking_id}"

    return {
        "tracking_id": tracking_id,
        "url": full_url
    }

# =========================
# 🧠 AI CORE
# =========================

def ai_engine(products, clicks):

    results = []

    for p in products:

        if "error" in p:
            continue

        score = p["score"]
        source = p["source"]

        # prediction
        boost = {"amazon":1.4, "check24":1.3, "tarifcheck":1.35}.get(source, 1.0)
        predicted = score * boost

        # decision
        if predicted > 130:
            action = "AUTO_SCALE"
        elif predicted > 100:
            action = "SCALE"
        elif predicted > 80:
            action = "HOLD"
        else:
            action = "CUT"

        # tracking
        tracking = generate_tracking_link(p["id"], source)

        # clicks
        product_clicks = [c for c in clicks if c["id"] == p["id"]]

        revenue = len(product_clicks) * predicted * 0.1

        results.append({
            "product": p,
            "predicted_score": round(predicted,2),
            "action": action,
            "tracking": tracking,
            "clicks": len(product_clicks),
            "revenue_estimate": round(revenue,2)
        })

    return results

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP H REAL DEPLOYMENT ENGINE LIVE 🚀"

@app.route("/run")
def run():

    products = sheets()
    clicks = load(CLICK_FILE)

    result = ai_engine(products, clicks)

    return jsonify({
        "status": "success",
        "mode": "STEP_H_PRODUCTION_LAYER",
        "results": result
    })

# =========================
# 🔗 CLICK TRACKING
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
        "total_clicks": len(clicks)
    })

# =========================
# 📊 TRACKING OVERVIEW
# =========================

@app.route("/tracking")
def tracking():

    return jsonify({
        "clicks": load(CLICK_FILE),
        "system": "STEP_H_ACTIVE"
    })

# =========================
# 🧠 HEALTH
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP_H"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
