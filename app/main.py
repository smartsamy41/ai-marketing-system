from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# =========================
# SERVICES (MINIMAL CORE ONLY)
# =========================

class Tracking:
    def track_click(self, product_id, source="api"):
        return {"product_id": product_id, "source": source}

class Landingpage:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

class SalesAPI:
    def send_lead(self, product_id, source="api"):
        return {
            "product_id": product_id,
            "status": "SENT",
            "source": source
        }

tracking = Tracking()
landingpage = Landingpage()
sales = SalesAPI()

# =========================
# MASTER ORCHESTRATOR
# =========================

from engine.orchestrator_clean_master import OrchestratorCleanMaster

orchestrator = OrchestratorCleanMaster(
    landingpage=landingpage,
    tracking=tracking,
    sales=sales
)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "ORCHESTRATOR CLEAN MASTER V1"
    }

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# RUN (MAIN FLOW)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:
        results.append(orchestrator.run(p))

    return {
        "status": "RUN_OK",
        "results": results,
        "report": orchestrator.report(),
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):
    return orchestrator.run(product_id)

# =========================
# REPORT
# =========================

@app.get("/report")
def report():
    return orchestrator.report()

# =========================
# RESET
# =========================

@app.get("/reset")
def reset():
    return orchestrator.reset()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "report": orchestrator.report(),
        "system": "MASTER ORCHESTRATOR ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
