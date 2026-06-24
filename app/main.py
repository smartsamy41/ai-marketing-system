from fastapi import FastAPI

# =========================
# SAFE IMPORT ORCHESTRATOR
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
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "orchestrator": run_orchestrator is not None
    }


# =========================
# RUN ORCHESTRATOR (LIVE MODE)
# =========================
@app.get("/run")
def run():

    # =========================
    # SAMPLE JOB LIST (LIVE SIMULATION)
    # =========================
    jobs = [
        {"product_id": "CHK24_001", "category": "check24", "data": {}},
        {"product_id": "TC_001", "category": "tarifcheck", "data": {}},
        {"product_id": "AMZ_001", "category": "amazon", "data": {}}
    ]

    results = []

    # =========================
    # ORCHESTRATOR EXECUTION
    # =========================
    if not run_orchestrator:
        return {
            "status": "ERROR",
            "message": "orchestrator not loaded"
        }

    for job in jobs:

        try:
            result = run_orchestrator(job)

            results.append({
                "product_id": job["product_id"],
                "status": "SUCCESS",
                "result": result
            })

        except Exception as e:

            results.append({
                "product_id": job["product_id"],
                "status": "ERROR",
                "message": str(e)
            })

    return {
        "status": "RUNNING_ORCHESTRATOR",
        "total_jobs": len(results),
        "results": results
    }


# =========================
# ENGINE CHECK
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "ENGINE OK",
        "orchestrator_loaded": run_orchestrator is not None
    }
