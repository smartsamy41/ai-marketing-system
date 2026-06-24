from fastapi import FastAPI, Request
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3

app = FastAPI()

# =========================
# INIT SYSTEM
# =========================

conversion = ConversionTrackingV3()


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "CONVERSION V3 ACTIVE"}


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


# =========================
# CLICK TRACK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return conversion.track_click(
        data.get("product_id"),
        "api"
    )


# =========================
# SALES / LEAD SIMULATION
# =========================

@app.get("/lead/{product_id}")
def lead(product_id: str):

    return conversion.track_lead(product_id)


# =========================
# CONVERSION (REAL MONEY EVENT)
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):

    # Simulated revenue (später Tarifcheck API)
    revenue = 12.5

    return conversion.track_conversion(product_id, revenue)


# =========================
# PRODUCT SCORE (AI ENGINE INPUT)
# =========================

@app.get("/score/{product_id}")
def score(product_id: str):

    return conversion.product_score(product_id)


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "system": "V3",
        "report": conversion.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# AUTOPILOT FLOW SIM (SAFE)
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "autopilot")
    conversion.track_lead("CHK24_001", "sales_api")
    conversion.track_conversion("CHK24_001", 15.0)

    return {
        "status": "AUTOPILOT_V3_DONE",
        "score": conversion.product_score("CHK24_001")
    }
