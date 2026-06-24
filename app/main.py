from fastapi import FastAPI
from datetime import datetime

from engine.landingpage_engine_v2 import LandingpageEngineV2
from engine.content_run_v1 import ContentRunV1

app = FastAPI()

# =========================
# INIT SYSTEM
# =========================

landingpage = LandingpageEngineV2()
content = ContentRunV1(landingpage)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "CONTENT RUN V1 ACTIVE"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RESET (CLEAN START)
# =========================

@app.get("/reset")
def reset():
    landingpage.reset()
    return {"status": "SYSTEM_RESET_DONE"}

# =========================
# RUN SINGLE PRODUCT
# =========================

@app.get("/run/{product_id}")
def run(product_id: str):

    return content.generate(product_id)

# =========================
# RUN FULL BATCH (CONTROLLED 1X FLOW)
# =========================

@app.get("/run-batch")
def run_batch():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return content.run_batch(products)

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "content": content.report(),
        "timestamp": datetime.utcnow().isoformat()
    }
