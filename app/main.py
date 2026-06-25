from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster

app = Fasfrom fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster

app = FastAPI()

# =========================
# INIT ORCHESTRATOR
# =========================
orchestrator = OrchestratorCleanMaster()

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE MODE ACTIVE"}

# =========================
# HEALTH CHECK
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
    }tAPI()

# =========================
# INIT ORCHESTRATOR
# =========================
orchestrator = OrchestratorCleanMaster()

# =========================
# BASE ROUTES
# =========================
@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE MODE ACTIVE"}

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
