from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster
from engine.dashboard_live_engine import DashboardLiveEngine

app = FastAPI()

# =========================
# INIT SYSTEM
# =========================
orchestrator = OrchestratorCleanMaster()
dashboard = DashboardLiveEngine()

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE MODE ACTIVE"}

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "OK"}

# =========================
# LIVE RUN (REAL SYSTEM)
# =========================
@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = orchestrator.run_all(products)

    return {
        "status": "RUNNING",
        "results": results
    }

# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
def get_dashboard():

    return dashboard.get_live()
