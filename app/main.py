from fastapi import FastAPI
from engine.orchestrator_engine_v2 import run_orchestrator
from engine.scheduler_engine import get_due_jobs

app = FastAPI()


@app.get("/")
def home():
    return {"status": "OK"}

@app.get("/run")
def run():

    jobs = get_due_jobs()

    results = []

    for job in jobs:

        result = run_orchestrator(job)

        results.append(result)

    return {
        "status": "RUNNING",
        "total_jobs": len(results),
        "results": results
    }
