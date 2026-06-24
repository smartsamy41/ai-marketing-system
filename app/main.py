from fastapi import FastAPI, Request
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v5_autonomy_engine import V5AutonomyEngine
from engine.v6_self_evolution_engine import V6SelfEvolutionEngine
from engine.v7_autonomous_business_engine import V7AutonomousBusiness
from engine.v8_self_rewriting_company import V8SelfRewritingCompany
from engine.v9_real_world_engine import V9RealWorldEngine

app = FastAPI()

# =========================
# INIT FULL STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v5 = V5AutonomyEngine(scaling, conversion)
v6 = V6SelfEvolutionEngine(v5, scaling, conversion)
v7 = V7AutonomousBusiness(v6, scaling, conversion)
v8 = V8SelfRewritingCompany(v7)
v9 = V9RealWorldEngine(conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V9 REAL WORLD ACTIVE"}


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


# =========================
# TRACK CLICK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return conversion.track_click(data.get("product_id"), "api")


# =========================
# CONVERT (REAL EVENT)
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):

    return conversion.track_conversion(product_id, 50.0)


# =========================
# SEND TO SALES API (REAL LAYER)
# =========================

@app.get("/sales/send/{product_id}")
def send_sales(product_id: str):

    return v9.send_to_sales_api(product_id)


# =========================
# REAL REVENUE CONFIRMATION
# =========================

@app.get("/sales/confirm/{product_id}/{revenue}")
def confirm(product_id: str, revenue: float):

    return v9.confirm_conversion(product_id, revenue)


# =========================
# REAL WORLD SCORE
# =========================

@app.get("/score")
def score():

    return v9.score()


# =========================
# SCALING DECISION
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):

    return scaling.analyze_product(product_id)


# =========================
# V9 FULL CYCLE
# =========================

@app.get("/v9/run")
def v9_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    # STEP 1: simulate sales API push
    for p in products:
        v9.send_to_sales_api(p)

    # STEP 2: conversion tracking
    conversion.track_click("CHK24_001", "v9")
    conversion.track_lead("CHK24_001", "v9")
    conversion.track_conversion("CHK24_001", 60.0)

    return {
        "status": "V9_REAL_WORLD_CYCLE_DONE",
        "score": v9.score(),
        "sales": v9.report(),
        "scaling": scaling.analyze_product("CHK24_001")
    }


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "sales": v9.report(),
        "score": v9.score(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# SAFE RUN
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v9")
    conversion.track_lead("CHK24_001", "v9")
    conversion.track_conversion("CHK24_001", 60.0)

    v9.send_to_sales_api("CHK24_001")

    return {
        "status": "V9_CYCLE_DONE",
        "score": v9.score(),
        "sales": v9.report()
    }
