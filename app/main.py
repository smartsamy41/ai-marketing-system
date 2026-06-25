from fastapi import FastAPI

from engine.orchestrator_clean_master import OrchestratorCleanMaster
from engine.dashboard_live_engine import DashboardLiveEngine
from engine.tarifcheck_sales_engine import TarifcheckSalesEngine

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
    return {
        "status": "OK",
        "system": "LIVE STABLE MODE"
    }

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK"
    }

# =========================
# MAIN ORCHESTRATOR RUN
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

# =========================
# PHASE 2 SALES TEST
# =========================
@app.get("/test-sales")
def test_sales():

    engine = TarifcheckSalesEngine()
    result = engine.fetch_leads()

    return {
        "status": "PHASE_2_SALES_TEST",
        "result": result
    }
