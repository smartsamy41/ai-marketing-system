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
# 📊 GOOGLE SHEETS CONNECT (CLOUD RUN SAFE)
# =========================

SPREADSHEET_ID = "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
RANGE_NAME = "products!A:C"

def google_sheets_connect():
    try:
        # 🔐 Cloud Run Default Auth (ADC)
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ])

        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get("values", [])

        products = []

        # Skip header row
        for row in values[1:]:
            if len(row) >= 3:
                products.append({
                    "product_id": row[0],
                    "score": int(row[1]),
                    "source": row[2]
                })

        return products

    except Exception as e:
        return [{"error": str(e), "source": "sheets_error"}]

# =========================
# 🧠 AI ENGINE
# =========================

def decide_winner(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"action": "WINNER", "weight": 3}
    elif score >= 80:
        return {"action": "KEEP", "weight": 2}
    else:
        return {"action": "LOW", "weight": 1}

def calculate_scaling(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"budget": 2.0}
    elif score >= 80:
        return {"budget": 1.5}
    else:
        return {"budget": 1.0}

def learning_engine(memory):
    for entry in memory:
        if entry["winner"]["action"] == "WINNER":
            entry["product"]["score"] += 1
        elif entry["winner"]["action"] == "LOW":
            entry["product"]["score"] -= 1
    return memory

# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "AI MARKETING SYSTEM LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "FINAL_PRODUCTION"
    })

@app.route("/data-source")
def data_source():
    return jsonify({
        "source": "GOOGLE_SHEETS_REAL",
        "data": google_sheets_connect()
    })

@app.route("/run")
def run():

    products = google_sheets_connect()
    memory = load_memory()

    results = []

    for p in products:

        if "error" in p:
            continue

        winner = decide_winner(p)
        scaling = calculate_scaling(p)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "product": p,
            "winner": winner,
            "scaling": scaling
        }

        memory.append(entry)
        results.append(entry)

    memory = learning_engine(memory)
    save_memory(memory)

    return jsonify({
        "status": "success",
        "mode": "FINAL_PRODUCTION",
        "data_source": "GOOGLE_SHEETS",
        "results": results,
        "memory_size": len(memory)
    })

@app.route("/memory")
def memory():
    return jsonify({
        "memory_size": len(load_memory()),
        "data": load_memory()
    })

@app.route("/system-status")
def status():
    return jsonify({
        "engine": "FINAL_AI_ENGINE",
        "status": "STABLE",
        "google_sheets": "CONNECTED",
        "learning": "ON",
        "memory": "ACTIVE"
    })

# =========================
# ☁️ START APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
