from fastapi import FastAPI, Request
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v9_real_world_engine import V9RealWorldEngine
from engine.v10_money_machine import V10MoneyMachine
from engine.v11_cloud_autopilot import V11CloudAutopilot

app = FastAPI()

# =========================
# INIT FULL STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v9 = V9RealWorldEngine(conversion)
v10 = V10MoneyMachine(v9, conversion)
v11 = V11CloudAutopilot(v10, v9, scaling)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V11 CLOUD AUTOPILOT ACTIVE"}


# =========================
# HEALTH (CLOUD RUN SAFE)
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
    return conversion.track_conversion(product_id, 100.0)


# =========================
# SCALING ENGINE
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# V10 MONEY ENGINE
# =========================

@app.get("/money/{product_id}")
def money(product_id: str):
    return v10.run_cycle(product_id)


# =========================
# V11 CLOUD AUTOPILOT (CORE)
# =========================

@app.get("/cloud/run")
def cloud_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return v11.scheduler_run(products)


# =========================
# SINGLE CLOUD CYCLE
# =========================

@app.get("/cloud/cycle/{product_id}")
def cloud_cycle(product_id: str):

    return v11.run_cloud_cycle(product_id)


# =========================
# CLOUD REPORT
# =========================

@app.get("/cloud/report")
def cloud_report():

    return v11.report()


# =========================
# DASHBOARD (FULL SYSTEM VIEW)
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "v9": v9.report(),
        "v10": v10.report(),
        "v11": v11.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# AUTOPILOT ENTRY POINT
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v11")
    conversion.track_lead("CHK24_001", "v11")
    conversion.track_conversion("CHK24_001", 120.0)

    cloud_result = v11.run_cloud_cycle("CHK24_001")

    return {
        "status": "V11_AUTOPILOT_RUNNING",
        "cloud": cloud_result
    }
