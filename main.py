from flask import Flask, jsonify
import os
import json
from datetime import datetime

# =========================
# 🟢 GOOGLE SHEETS IMPORT (SAFE TRY)
# =========================

try:
    from google.oauth2.service_account import Credentials
    import gspread
    SHEETS_ENABLED = True
except:
    SHEETS_ENABLED = False

app = Flask(__name__)

# =========================
# 💾 MEMORY FILE (FALLBACK)
# =========================

MEMORY_FILE = "memory.json"

# =========================
# 🧠 MEMORY LOAD
# =========================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# 🌐 REAL GOOGLE SHEETS CONNECT
# =========================

def google_sheets_connect():

    if not SHEETS_ENABLED:
        # fallback safe mode
        return [
            {"product_id": "AMZ_001", "score": 95, "source": "fallback"},
            {"product_id": "CHK24_001", "score": 87, "source": "fallback"},
            {"product_id": "TC_001", "score": 76, "source": "fallback"}
        ]

    try:
        # 🔐 SERVICE ACCOUNT FILE
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=scope
        )

        client = gspread.authorize(creds)

        # 📊 SHEET OPEN
        sheet = client.open("AI_Marketing_System").worksheet("products")

        data = sheet.get_all_records()

        return data

    except Exception as e:
        return [{"error": str(e), "source": "sheets_error"}]

# =========================
# 🧠 WINNER ENGINE
# =========================

def decide_winner(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"action": "WINNER", "weight": 3}
    elif score >= 80:
        return {"action": "KEEP", "weight": 2}
    else:
        return {"action": "LOW", "weight": 1}

# =========================
# 📈 SCALING ENGINE
# =========================

def calculate_scaling(product):
    score = product.get("score", 0)

    if score >= 90:
        return {"budget": 2.0}
    elif score >= 80:
        return {"budget": 1.5}
    else:
        return {"budget": 1.0}

# =========================
# 🧠 LEARNING ENGINE
# =========================

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
    return "AI ENGINE STEP 7 GOOGLE SHEETS API LIVE 🚀"

@app.route("/run")
def run():

    # 🌐 REAL DATA FROM SHEETS
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

    # 🧠 LEARNING
    memory = learning_engine(memory)

    # 💾 SAVE MEMORY
    save_memory(memory)

    return jsonify({
        "status": "success",
        "mode": "STEP_7_GOOGLE_SHEETS_API",
        "data_source": "REAL_SHEETS" if SHEETS_ENABLED else "FALLBACK",
        "results": results,
        "memory_size": len(memory),
        "sheets_enabled": SHEETS_ENABLED
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
        "engine": "STEP7_SHEETS_API",
        "status": "STABLE",
        "google_sheets": SHEETS_ENABLED,
        "learning": "ON",
        "memory": "PERSISTENT"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "STEP7",
        "sheets_api": SHEETS_ENABLED
    })

# =========================
# ☁️ ENTRY
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
