from flask import Flask, jsonify
import os
import json
from datetime import datetime

import google.auth
from google.auth.transport.requests import Request
import gspread

app = Flask(__name__)

# =========================
# 💾 MEMORY FILE
# =========================

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# 🌐 DEFAULT AUTH GOOGLE SHEETS CONNECT
# =========================

def google_sheets_connect():
    try:
        # 🔐 DEFAULT CLOUD RUN AUTH
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ])

        client = gspread.authorize(creds)

        sheet = client.open("AI_Marketing_System").worksheet("products")

        data = sheet.get_all_records()

        return data

    except Exception as e:
        return [{"error": str(e), "source": "auth_failed"}]

# =========================
# 🧠 ENGINE LOGIC
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
    return "AI ENGINE DEFAULT AUTH LIVE 🚀"

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
        "mode": "DEFAULT_AUTH_ACTIVE",
        "data_source": "GOOGLE_SHEETS_REAL",
        "results": results,
        "memory_size": len(memory)
    })

@app.route("/data-source")
def data_source():
    return jsonify({
        "source": "GOOGLE_SHEETS_REAL",
        "data": google_sheets_connect()
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
        "engine": "DEFAULT_AUTH_MODE",
        "status": "STABLE",
        "auth": "CLOUD_RUN_ADC",
        "learning": "ON",
        "memory": "PERSISTENT"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "DEFAULT_AUTH"
    })

# =========================
# ☁️ ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
