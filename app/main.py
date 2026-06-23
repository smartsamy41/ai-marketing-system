
from fastapi import FastAPI

from engine.orchestrator_engine_v2 import run_orchestrator
from engine.scheduler_engine import get_due_jobs

app = FastAPI()


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {
        "status": "OK",
        "system": "AI MARKETING RUNNING",
        "mode": "PRODUCTION"
    }


# =========================
# RUN
# =========================
@app.get("/run")
def run():

    jobs = get_due_jobs()

    results = []

    for job in jobs:

        clean_job = {
            "product_id": job.get("product_id"),
            "category": job.get("category", "default"),
            "data": job.get("data", {})
        }

        try:
            result = run_orchestrator(clean_job)

            results.append({
                "product": clean_job["product_id"],
                "status": "SUCCESS",
                "result": result
            })

        except Exception as e:

            results.append({
                "product": clean_job["product_id"],
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "executed": len(results),
        "results": results
    }
