from fastapi import FastAPI
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v5_autonomy_engine import V5AutonomyEngine

app = FastAPI()

# =========================
# INIT SYSTEM STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v5 = V5AutonomyEngine(scaling, conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V5 AUTONOMY ACTIVE"}


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
async def track(request):
    data = await request.json()
    return conversion.track_click(data.get("product_id"), "api")


# =========================
# CONVERT
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):
    return conversion.track_conversion(product_id, 20.0)


# =========================
# SCALING V4
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# V5 AUTONOMY CORE
# =========================

@app.get("/v5/run")
def v5_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return v5.run_cycle(products)


# =========================
# LEARNING DASHBOARD
# =========================

@app.get("/v5/learn")
def v5_learn():

    return v5.learn()


# =========================
# DECISION ENGINE
# =========================

@app.get("/v5/decide")
def v5_decide():

    return v5.decide_next_action()


# =========================
# FULL DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "scaling": scaling.report(),
        "v5_learning": v5.learn(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# AUTOPILOT RUN (SAFE ENTRY)
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v5")
    conversion.track_lead("CHK24_001", "v5")
    conversion.track_conversion("CHK24_001", 25.0)

    scale = scaling.analyze_product("CHK24_001")
    learn = v5.observe("CHK24_001")

    return {
        "status": "V5_CYCLE_DONE",
        "scale": scale,
        "learning": learn
    }
