from fastapi import FastAPI

# =========================
# SAFE IMPORT LAYER
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
except Exception:
    run_orchestrator = None


app = FastAPI()


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "LIVE"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "orchestrator_loaded": run_orchestrator is not None
    }


# =========================
# RUN SYSTEM
# =========================
@app.get("/run")
def run():

    job = {
        "product_id": "TEST_001",
        "category": "default",
        "data": {}
    }

    # -------------------------
    # ORCHESTRATOR CHECK
    # -------------------------
    if not run_orchestrator:
        return {
            "status": "ERROR",
            "message": "orchestrator not loaded"
        }

    # -------------------------
    # SAFE EXECUTION
    # -------------------------
    try:
        result = run_orchestrator(job)

        return {
            "status": "RUN OK",
            "result": result
        }

    except Exception as error:
        return {
            "status": "RUN ERROR",
            "message": str(error)
        }


# =========================
# ENGINE TEST
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "ENGINE OK",
        "orchestrator": run_orchestrator is not None
    }
