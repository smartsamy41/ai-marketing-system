from fastapi import FastAPI
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v5_autonomy_engine import V5AutonomyEngine
from engine.v6_self_evolution_engine import V6SelfEvolutionEngine

app = FastAPI()

# =========================
# INIT STACK
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)
v5 = V5AutonomyEngine(scaling, conversion)
v6 = V6SelfEvolutionEngine(v5, scaling, conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V6 SELF EVOLUTION ACTIVE"}


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
    return conversion.track_conversion(product_id, 25.0)


# =========================
# SCALING
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# V6 EVOLUTION CORE
# =========================

@app.get("/v6/run")
def v6_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return v6.run(products)


# =========================
# V6 REPORT
# =========================

@app.get("/v6/report")
def v6_report():

    return v6.report()


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "scaling": scaling.report(),
        "v5": v5.learn(),
        "v6": v6.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# SAFE AUTOPILOT ENTRY
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v6")
    conversion.track_lead("CHK24_001", "v6")
    conversion.track_conversion("CHK24_001", 30.0)

    scale = scaling.analyze_product("CHK24_001")
    v5_state = v5.observe("CHK24_001")
    v6_state = v6.run(["CHK24_001", "TC_001"])

    return {
        "status": "V6_CYCLE_DONE",
        "scale": scale,
        "v5": v5_state,
        "v6": v6_state
    }
