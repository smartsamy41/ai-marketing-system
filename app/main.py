from fastapi import FastAPI
from datetime import datetime

from engine.landingpage_engine_v2 import LandingpageEngineV2
from engine.content_run_v1 import ContentRunV1
from engine.scheduler_v1 import SchedulerV1

app = FastAPI()

# =========================
# INIT SYSTEM
# =========================

landingpage = LandingpageEngineV2()
content = ContentRunV1(landingpage)
scheduler = SchedulerV1(content)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "SCHEDULER V1 ACTIVE"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RESET SYSTEM
# =========================

@app.get("/reset")
def reset():
    landingpage.reset()
    return {"status": "RESET_DONE"}

# =========================
# SCHEDULER RUN (CORE)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001", "CHK24_002", "TC_002"]

    return scheduler.run(products)

# =========================
# MORNING RUN ONLY
# =========================

@app.get("/run/morning")
def morning():

    return scheduler.run(["CHK24_001", "TC_001", "AMZ_001"])

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "scheduler": scheduler.report(),
        "timestamp": datetime.utcnow().isoformat()
    }
