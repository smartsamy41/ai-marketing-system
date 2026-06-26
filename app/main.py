from fastapi import FastAPI

from engine.orchestrator_clean_master import OrchestratorCleanMaster

app = FastAPI()

orchestrator = OrchestratorCleanMaster()


@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "ORCHESTRATOR ACTIVE"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/run")
def run():
    return orchestrator.run_all(None)
