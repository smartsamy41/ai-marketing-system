from fastapi import FastAPI, Request
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v9_real_world_engine import V9RealWorldEngine
from engine.v10_money_machine import V10MoneyMachine
from engine.v11_cloud_autopilot import V11CloudAutopilot
from engine.v12_business_os import V12BusinessOS

app = FastAPI()

# =========================
# INIT FULL STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v9 = V9RealWorldEngine(conversion)
v10 = V10MoneyMachine(v9, conversion)
v11 = V11CloudAutopilot(v10, v9, scaling)
v12 = V12BusinessOS(v11, v10, scaling)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V12 BUSINESS OS ACTIVE"}


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
    return conversion.track_conversion(product_id, 100.0)


# =========================
# SCALING
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# CLOUD AUTOPILOT
# =========================

@app.get("/cloud/{product_id}")
def cloud(product_id: str):
    return v11.run_cloud_cycle(product_id)


# =========================
# MONEY ENGINE
# =========================

@app.get("/money")
def money():
    return v10.report()


# =========================
# BUSINESS OS CORE
# =========================

@app.get("/v12/run/{product_id}")
def v12_run(product_id: str):

    return v12.run(product_id)


# =========================
# BUSINESS DECISION
# =========================

@app.get("/v12/decision/{product_id}")
def v12_decision(product_id: str):

    v12.collect(product_id)
    return v12.decide()


# =========================
# DASHBOARD (FULL CONTROL TOWER)
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "v10": v10.report(),
        "v11": v11.report(),
        "v12": v12.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# AUTOPILOT ENTRY
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v12")
    conversion.track_lead("CHK24_001", "v12")
    conversion.track_conversion("CHK24_001", 100.0)

    result = v12.run("CHK24_001")

    return {
        "status": "V12_BUSINESS_OS_RUNNING",
        "result": result
    }
