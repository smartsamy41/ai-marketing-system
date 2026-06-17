from flask import Flask, jsonify
import os
import json
from datetime import datetime

import google.auth
from googleapiclient.discovery import build

app = Flask(__name__)

# =========================
# CONFIG
# =========================

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"

PRODUCT_RANGE = "products!A:D"
ASSET_RANGE = "affiliate_assets!A:E"

MEMORY_FILE = "memory.json"

# =========================
# MEMORY
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
# GOOGLE SHEETS
# =========================

def sheets(range_name):
    try:
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets"
        ])

        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        return result.get("values", [])

    except Exception as e:
        return [["error", str(e)]]

# =========================
# PRODUCTS
# =========================

def get_products():
    rows = sheets(PRODUCT_RANGE)
    products = []

    for r in rows[1:]:

        try:
            products.append({
                "product_id": r[0],
                "score": float(r[1]) if len(r) > 1 and r[1] != "" else 50,
                "source": r[2] if len(r) > 2 else "unknown",
                "status": r[3] if len(r) > 3 else "active"
            })
        except:
            continue

    return products

# =========================
# ASSETS
# =========================

def get_assets():
    rows = sheets(ASSET_RANGE)
    assets = []

    for r in rows[1:]:

        try:
            assets.append({
                "product_id": r[0],
                "source": r[1],
                "type": r[2],
                "url": r[3],
                "tracking": r[4] if len(r) > 4 else ""
            })
        except:
            continue

    return assets

# =========================
# SCORING ENGINE
# =========================

def score_product(product):

    boost_map = {
        "amazon": 1.4,
        "check24": 1.25,
        "tarifcheck": 1.3,
        "telekom": 1.6
    }

    base = product["score"]
    source = product["source"]

    return base * boost_map.get(source, 1.0)

# =========================
# ROUTING
# =========================

def route(source):

    return {
        "amazon": "pinterest",
        "check24": "youtube",
        "tarifcheck": "blog",
        "telekom": "shop"
    }.get(source, "unknown")

# =========================
# ASSET MATCH
# =========================

def match_asset(product_id, source, assets):

    for a in assets:
        if a["product_id"] == product_id and a["source"] == source:
            return a["url"]

    return None

# =========================
# ENGINE
# =========================

def run_engine():

    products = get_products()
    assets = get_assets()
    memory = load_memory()

    results = []

    for p in products:

        if p["status"] != "active":
            continue

        final_score = score_product(p)
        channel = route(p["source"])
        asset = match_asset(p["product_id"], p["source"], assets)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "product_id": p["product_id"],
            "source": p["source"],
            "final_score": round(final_score, 2),
            "channel": channel,
            "asset_url": asset,
            "ready": asset is not None
        }

        results.append(entry)
        memory.append(entry)

    save_memory(memory)

    return results

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return "CLEAN AI MARKETING SYSTEM V1 LIVE 🚀"

@app.route("/run")
def run():
    return jsonify({
        "status": "ok",
        "mode": "CLEAN_V1",
        "data": run_engine()
    })

@app.route("/products")
def products():
    return jsonify(get_products())

@app.route("/assets")
def assets():
    return jsonify(get_assets())

@app.route("/debug")
def debug():
    return jsonify({
        "products": len(get_products()),
        "assets": len(get_assets()),
        "sample_products": get_products()[:3],
        "sample_assets": get_assets()[:3]
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "CLEAN_V1_STABLE"
    })

# =========================
# START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
