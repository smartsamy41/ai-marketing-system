from fastapi import FastAPI

# =========================
# SAFE IMPORT LAYER
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
except Exception as e:
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
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "orchestrator_loaded": run_orchestrator is not None
    }


# =========================
# RUN (SAFE MODE - NO CRASH)
# =========================
@app.get("/run")
def run():

    job = {
        "product_id": "TEST_001",
        "category": "default",
        "data": {}
    }

    # IF ORCHESTRATOR NOT LOADED
    if not run_orchestrator:
        return {
            "status": "ERROR",
            "message": "orchestrator not loaded"
        }

    try:
        result = run_orchestrator(job)

        return {
            "status": "RUN OK",
            "result": result
        }

    except Exception as e:
        return {
            "status": "RUN ERROR",
            "message": str(e)
        }


# =========================
# DEBUG ENGINE TEST
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "ENGINE OK",
        "orchestrator": run_orchestrator is not None
    }
