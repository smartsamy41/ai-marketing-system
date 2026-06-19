from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

print("🟢 AI SYSTEM STARTED (CLEAN MAIN)")

# =========================
# 🧠 SAFE ENGINE LOADING
# =========================

try:
    from engine.master_engine import MasterEngine
except Exception as e:
    print("⚠️ MasterEngine not loaded:", e)
    MasterEngine = None

try:
    from engine.orchestrator_engine import OrchestratorEngine
except Exception as e:
    print("⚠️ OrchestratorEngine not loaded:", e)
    OrchestratorEngine = None

try:
    from engine.content_engine import ContentEngine
except Exception as e:
    print("⚠️ ContentEngine not loaded:", e)
    ContentEngine = None


# =========================
# 🔵 INIT SAFE INSTANCES
# =========================

master = MasterEngine() if MasterEngine else None
orchestrator = OrchestratorEngine() if OrchestratorEngine else None
content = ContentEngine() if ContentEngine else None


# =========================
# 🟢 ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "AI SYSTEM ONLINE",
        "time": str(datetime.now())
    }


# =========================
# 🟢 HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "RUNNING",
        "system": "CLEAN_APP_MAIN",
        "time": str(datetime.now())
    }


# =========================
# 🚀 TEST PIPELINE (SAFE)
# =========================

@app.get("/run")
def run():

    products = [
        "Strom Vergleich",
        "Gas Anbieter",
        "DSL Internet"
    ]

    results = []

    for p in products:

        data = {
            "product": p,
            "title": f"{p} 2026 Vergleich",
            "blog": f"Automatisierter Content für {p}",
            "timestamp": str(datetime.now())
        }

        results.append(data)

    return {
        "status": "SUCCESS",
        "count": len(results),
        "results": results
    }
