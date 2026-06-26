from fastapi import FastAPI

from engine.orchestrator_clean_master import OrchestratorCleanMaster

app = FastAPI()

orchestrator = OrchestratorCleanMaster()

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "SAFE MODE ACTIVE"
    }

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK"
    }

# =========================
# RUN PIPELINE (SAFE ONLY)
# =========================
@app.get("/run")
def run():
    return orchestrator.execute_real_publish()
