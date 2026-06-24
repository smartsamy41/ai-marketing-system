from fastapi import FastAPI, Request
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v9_real_world_engine import V9RealWorldEngine
from engine.v10_money_machine import V10MoneyMachine

app = FastAPI()

# =========================
# INIT STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v9 = V9RealWorldEngine(conversion)
v10 = V10MoneyMachine(v9, conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V10 MONEY MACHINE ACTIVE"}


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


# =========================
# TRACK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return conversion.track_click(data.get("product_id"), "api")


# =========================
# CONVERT
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):

    return conversion.track_conversion(product_id, 70.0)


# =========================
# V9 SALES CONNECT
# =========================

@app.get("/sales/{product_id}")
def sales(product_id: str):

    return v9.send_to_sales_api(product_id)


# =========================
# V10 INGEST REAL MONEY
# =========================

@app.get("/money/{product_id}")
def money(product_id: str):

    return v10.run_cycle(product_id)


# =========================
# V10 ANALYTICS
# =========================

@app.get("/analytics")
def analytics():

    return v10.analyze()


# =========================
# V10 ALLOCATION ENGINE
# =========================

@app.get("/allocate")
def allocate():

    return v10.allocate()


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "v9": v9.report(),
        "v10": v10.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# MAIN RUN (AUTOPILOT ENTRY)
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v10")
    conversion.track_lead("CHK24_001", "v10")
    conversion.track_conversion("CHK24_001", 80.0)

    v9.ingest("CHK24_001", 80.0)

    v10_result = v10.run_cycle("CHK24_001")

    return {
        "status": "V10_MONEY_MACHINE_RUNNING",
        "v10": v10_result,
        "timestamp": datetime.utcnow().isoformat()
    }
