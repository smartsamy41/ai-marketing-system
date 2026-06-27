from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster

app = FastAPI()

orchestrator = OrchestratorCleanMaster()


@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "AI_MARKETING_SYSTEM_RELEASE_1",
        "mode": "PRODUCTION_AUDIT_READY"
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True
    }


@app.get("/run")
def run():
    return orchestrator.run_pipeline()


@app.get("/audit/sheet")
def audit_sheet():
    return orchestrator.run_sheet_audit()
