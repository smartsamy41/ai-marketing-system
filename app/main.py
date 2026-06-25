from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster
from engine.dashboard_live_engine import DashboardLiveEngine

app = FastAPI()

orchestrator = OrchestratorCleanMaster()
dashboard = DashboardLiveEngine()

@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE MODE ACTIVE"}

@app.get("/run")
def run():
    products = ["CHK24_001", "TC_001", "AMZ_001"]
    return orchestrator.run_all(products)

@app.get("/health")
def health():
    return {"status": "OK"}
