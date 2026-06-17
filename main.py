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
# 💰 STEP A (AFFILIATE SCORE)
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
# 🧠 STEP B (LEARNING ENGINE)
# =========================

def learning_engine(memory):
    """
    STEP B: AI lernt aus Performance
    """

    product_stats = {}

    # 1. Statistik sammeln
    for entry in memory:
        pid = entry["product"]["product_id"]

        if pid not in product_stats:
            product_stats[pid] = {
                "wins": 0,
                "losses": 0,
                "avg_score": entry["product"]["score"]
            }

        if entry["budget"]["level"] == "HIGH_SCALE":
            product_stats[pid]["wins"] += 1
        elif entry["budget"]["level"] == "HOLD":
            product_stats[pid]["losses"] += 1

    # 2. Lern-Boost berechnen
    for entry in memory:
        pid = entry["product"]["product_id"]

        stats = product_stats.get(pid, {})

        win_rate = 0
        if stats.get("wins", 0) + stats.get("losses", 0) > 0:
            win_rate = stats.get("wins", 0) / (stats.get("wins", 0) + stats.get("losses", 0))

        # 🔥 LEARNING SCORE ADJUSTMENT
        if win_rate > 0.6:
            entry["product"]["score"] += 2
        elif win_rate < 0.3:
            entry["product"]["score"] -= 2

    return memory

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "STEP B AI LEARNING ENGINE LIVE 🚀"

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
            "score_data": score_data,
            "budget": budget
        }

        memory.append(entry)
        results.append(entry)

    # 🧠 STEP B LEARNING APPLY
    memory = learning_engine(memory)

    save_memory(memory)

    return jsonify({
        "status": "success",
        "mode": "STEP_B_LEARNING_ENGINE",
        "results": results,
        "memory_size": len(memory)
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
        "version": "STEP_B"
    })

# =========================
# ☁️ START
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
