from flask import Flask, jsonify
import os
import json
from datetime import datetime

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# 📦 CONFIG
# =========================

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
PRODUCT_RANGE = "products!A:D"
ASSET_RANGE = "affiliate_assets!A:E"

MEMORY_FILE = "memory.json"

# =========================
# 💾 MEMORY
# =========================

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

def sheets_connect(range_name):
    try:
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ])

        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        values = result.get("values", [])

        return values

    except Exception as e:
        return [["error", str(e)]]

# =========================
# 📦 PRODUCT LOADER
# =========================

def get_products():

    rows = sheets_connect(PRODUCT_RANGE)
    products = []

    for r in rows[1:]:

        product_id = r[0] if len(r) > 0 else "unknown"

        try:
            score = float(r[1])
        except:
            score = 50

        source = r[2] if len(r) > 2 else "unknown"

        status = r[3] if len(r) > 3 else "active"

        products.append({
            "product_id": product_id,
            "score": score,
            "source": source,
            "status": status
        })

    return products

# =========================
# 🎯 ASSET LOADER
# =========================

def get_assets():

    rows = sheets_connect(ASSET_RANGE)
    assets = []

    for r in rows[1:]:

        assets.append({
            "product_id": r[0],
            "source": r[1],
            "type": r[2],
            "url": r[3],
            "tracking": r[4] if len(r) > 4 else ""
        })

    return assets

# =========================
# 🔥 ENGINE CORE
# =========================

def calculate_score(product):

    base = product["score"]
    source = product["source"]

    boost_map = {
        "amazon": 1.4,
        "check24": 1.3,
        "tarifcheck": 1.35,
        "telekom": 1.6
    }

    boost = boost_map.get(source, 1.0)

    return base * boost

# =========================
# 🧠 CHANNEL ROUTER
# =========================

def route(source):

    routing = {
        "amazon": {"channel": "pinterest", "format": "pin"},
        "check24": {"channel": "youtube", "format": "short"},
        "tarifcheck": {"channel": "blog", "format": "article"},
        "telekom": {"channel": "shop", "format": "direct"}
    }

    return routing.get(source, {"channel": "unknown", "format": "none"})

# =========================
# 🔗 ASSET MATCHER
# =========================

def match_asset(product_id, source, assets):

    for a in assets:
        if a["product_id"] == product_id and a["source"] == source:
            return a["url"]

    return None

# =========================
# 🚀 MAIN ENGINE
# =========================

def run_engine():

    products = get_products()
    assets = get_assets()
    memory = load_memory()

    results = []

    for p in products:

        if p["status"] != "active":
            continue

        final_score = calculate_score(p)
        channel = route(p["source"])
        asset_url = match_asset(p["product_id"], p["source"], assets)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "product": p,
            "final_score": round(final_score, 2),
            "channel": channel,
            "asset_url": asset_url,
            "ready": asset_url is not None
        }

        memory.append(entry)
        results.append(entry)

    save_memory(memory)

    return results

# =========================
# 🌐 ROUTES
# =========================

@app.route("/")
def home():
    return "CLEAN AI MARKETING SYSTEM RUNNING 🚀"

@app.route("/run")
def run():
    return jsonify({
        "status": "success",
        "data": run_engine()
    })

@app.route("/products")
def products():
    return jsonify(get_products())

@app.route("/assets")
def assets():
    return jsonify(get_assets())

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "CLEAN_V1"
    })

# =========================
# 🚀 START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
