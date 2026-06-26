from fastapi import FastAPI

from engine.orchestrator_clean_master import OrchestratorCleanMaster

# =========================
# APP INIT (CLOUD RUN SAFE)
# =========================
app = FastAPI()

orchestrator = OrchestratorCleanMaster()

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "LIVE",
        "system": "AI_MARKETING_SYSTEM",
        "mode": "PRODUCTION"
    }

# =========================
# HEALTH CHECK (CRITICAL FOR CLOUD RUN)
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True
    }

# =========================
# MAIN PIPELINE TRIGGER
# =========================
@app.get("/run")
def run():

    try:
        result = orchestrator.run_all()
        return result

    except Exception as e:

        return {
            "status": "CRASH_FIXED_SAFE_RETURN",
            "error": str(e)
        }
