
from fastapi import FastAPI
import time

from app.engine.orchestrator_engine import run_orchestrator
from app.engine.scheduler_engine import get_due_jobs

app = FastAPI()


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {
        "status": "CLOUD RUN ACTIVE",
        "system": "PRODUCTION V2",
        "mode": "AUTOPILOT READY"
    }


# =========================
# SINGLE RUN TRIGGER
# =========================
@app.get("/run")
def run_once():

    jobs = get_due_jobs()

    results = []

    for job in jobs:

        try:

            result = run_orchestrator(job)

            results.append({
                "job": job.get("product_id"),
                "status": "SUCCESS",
                "output": result
            })

        except Exception as e:

            results.append({
                "job": job.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "executed_jobs": len(results),
        "results": results
    }


# =========================
# AUTOPILOT LOOP (PRODUCTION MODE)
# =========================
@app.get("/autopilot")
def autopilot():

    cycle = 0

    while cycle < 1000:   # safety limit

        jobs = get_due_jobs()

        for job in jobs:

            try:
                run_orchestrator(job)

            except Exception as e:
                print("ERROR:", e)

        cycle += 1
        time.sleep(60)

    return {
        "status": "AUTOPILOT STOPPED (LIMIT REACHED)"
    }
