from fastapi import FastAPI

from engine.orchestrator_clean_master import OrchestratorCleanMaster
from engine.dashboard_live_engine import DashboardLiveEngine

app = FastAPI()

# =========================
# FINAL SYSTEM CONNECT
# =========================

orchestrator = OrchestratorCleanMaster()
dashboard = DashboardLiveEngine()

# =========================
# RUN SYSTEM
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "FINAL WIRED SYSTEM"}

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = orchestrator.run_all(products)

    return {
        "status": "RUNNING",
        "results": results
    }

@app.get("/dashboard")
def get_dashboard():

    return dashboard.get_live()
