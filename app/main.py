from fastapi import FastAPI
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v5_autonomy_engine import V5AutonomyEngine
from engine.v6_self_evolution_engine import V6SelfEvolutionEngine
from engine.v7_autonomous_business_engine import V7AutonomousBusiness

app = FastAPI()

# =========================
# INIT FULL STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v5 = V5AutonomyEngine(scaling, conversion)
v6 = V6SelfEvolutionEngine(v5, scaling, conversion)
v7 = V7AutonomousBusiness(v6, scaling, conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V7 AUTONOMOUS BUSINESS ACTIVE"}


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
async def track(request):
    data = await request.json()
    return conversion.track_click(data.get("product_id"), "api")


# =========================
# CONVERT
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):
    return conversion.track_conversion(product_id, 35.0)


# =========================
# SCALING
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# V7 AUTONOMOUS BUSINESS CORE
# =========================

@app.get("/v7/run")
def v7_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return v7.run(products)


# =========================
# V7 REPORT
# =========================

@app.get("/v7/report")
def v7_report():

    return v7.report()


# =========================
# DASHBOARD (FULL INTELLIGENCE)
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "scaling": scaling.report(),
        "v5": v5.learn(),
        "v6": v6.report(),
        "v7": v7.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# SAFE AUTOPILOT ENTRY
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v7")
    conversion.track_lead("CHK24_001", "v7")
    conversion.track_conversion("CHK24_001", 40.0)

    scale = scaling.analyze_product("CHK24_001")
    v6_state = v6.run(["CHK24_001", "TC_001"])
    v7_state = v7.run(["CHK24_001", "TC_001", "AMZ_001"])

    return {
        "status": "V7_BUSINESS_CYCLE_DONE",
        "scale": scale,
        "v7": v7_state
    }
