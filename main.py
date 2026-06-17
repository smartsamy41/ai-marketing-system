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

# =========================
# SHEETS CONNECT (SAFE)
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
# LOAD PRODUCTS
# =========================

def get_products():

    rows = sheets(PRODUCT_RANGE)
    products = []

    for r in rows[1:]:

        try:
            products.append({
                "product_id": r[0],
                "score": float(r[1]) if len(r) > 1 else 50,
                "source": r[2] if len(r) > 2 else "unknown",
                "status": r[3] if len(r) > 3 else "active"
            })
        except:
            continue

    return products

# =========================
# LOAD ASSETS
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
# SCORING ENGINE (STABLE)
# =========================

def score(product):

    boost = {
        "amazon": 1.4,
        "check24": 1.25,
        "tarifcheck": 1.3,
        "telekom": 1.6
    }

    return product["score"] * boost.get(product["source"], 1.0)

# =========================
# ROUTING ENGINE (STABLE)
# =========================

def route(source):

    mapping = {
        "amazon": "pinterest",
        "check24": "youtube",
        "tarifcheck": "blog",
        "telekom": "shop"
    }

    return mapping.get(source, "unknown")

# =========================
# ASSET MATCH
# =========================

def match_asset(product_id, source, assets):

    for a in assets:
        if a["product_id"] == product_id and a["source"] == source:
            return a["url"]

    return None

# =========================
# MAIN ENGINE (ONLY ONE FLOW)
# =========================

def run_engine():

    products = get_products()
    assets = get_assets()

    results = []

    for p in products:

        if p["status"] != "active":
            continue

        final_score = score(p)
        channel = route(p["source"])
        asset = match_asset(p["product_id"], p["source"], assets)

        results.append({
            "product_id": p["product_id"],
            "source": p["source"],
            "final_score": round(final_score, 2),
            "channel": channel,
            "asset": asset,
            "ready": asset is not None
        })

    return results

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return "CLEAN AI ENGINE RUNNING 🚀"

@app.route("/run")
def run():
    return jsonify({
        "status": "ok",
        "mode": "CLEAN_ENGINE_V1",
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
        "version": "CLEAN_V1_STABLE"
    })

# =========================
# START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
