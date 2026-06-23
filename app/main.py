from fastapi import FastAPI

# =========================
# SAFE ENGINE IMPORT LAYER
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
    from engine.scheduler_engine import SchedulerEngine
    from engine.core_engine import CoreEngine
except Exception as e:
    run_orchestrator = None
    SchedulerEngine = None
    CoreEngine = None


app = FastAPI()


# =========================
# CORE HEALTH
# =========================
@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE"}


@app.get("/health")
def health():
    return {
        "status": "OK",
        "engine_loaded": run_orchestrator is not None
    }


# =========================
# RUN SYSTEM
# =========================
@app.get("/run")
def run():

    if not run_orchestrator:
        return {"status": "ERROR", "message": "Engine not loaded"}

    # MOCK JOB (safe test)
    job = {
        "product_id": "TEST_001",
        "category": "default",
        "data": {}
    }

    result = run_orchestrator(job)

    return {
        "status": "RUNNING",
        "result": result
    }


# =========================
# ENGINE TEST
# =========================
@app.get("/engine")
def engine_test():

    core = CoreEngine() if CoreEngine else None

    if not core:
        return {"status": "ERROR", "message": "CoreEngine missing"}

    return core.health()
