from flask import Flask, jsonify
import os

app = Flask(__name__)

# =========================
# 🧠 SIMPLE AI LOGIC (STEP 1)
# =========================

def get_products():
    return [
        {"product_id": "AMZ_001", "score": 92},
        {"product_id": "CHK24_001", "score": 85},
        {"product_id": "TC_001", "score": 78}
    ]


# =========================
# 🧠 WINNER ENGINE (INLINE)
# =========================

def decide_winner(product):
    score = product.get("score", 0)

    if score >= 90:
        return {
            "action": "WINNER",
            "reason": "HIGH_SCORE"
        }
    elif score >= 80:
        return {
            "action": "KEEP",
            "reason": "STABLE"
        }
    else:
        return {
            "action": "LOW",
            "reason": "WEAK"
        }


# =========================
# 📈 SCALING ENGINE (INLINE)
# =========================

def calculate_scaling(product):
    score = product.get("score", 0)

    if score >= 90:
        return {
            "budget_multiplier": 2.0,
            "action": "AGGRESSIVE_SCALE"
        }
    elif score >= 80:
        return {
            "budget_multiplier": 1.5,
            "action": "NORMAL_SCALE"
        }
    else:
        return {
            "budget_multiplier": 1.0,
            "action": "NO_SCALE"
        }


# =========================
# 🚀 ROUTES
# =========================

@app.route("/")
def home():
    return "AI ENGINE V2 STEP 1 LIVE 🚀"

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "version": "V2_STEP1"
    })

@app.route("/run")
def run():

    products = get_products()

    results = []

    for p in products:

        winner = decide_winner(p)
        scaling = calculate_scaling(p)

        results.append({
            "product": p,
            "winner": winner,
            "scaling": scaling
        })

    return jsonify({
        "status": "success",
        "mode": "STEP_1_ENGINE",
        "results": results
    })

@app.route("/system-status")
def system_status():
    return jsonify({
        "cloud_run": "ONLINE",
        "engine": "STEP1_ACTIVE",
        "winner_engine": "INLINE",
        "scaling_engine": "INLINE",
        "status": "STABLE"
    })


# =========================
# ☁️ ENTRY POINT
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
