from fastapi import FastAPI
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4
from engine.v5_autonomy_engine import V5AutonomyEngine
from engine.v6_self_evolution_engine import V6SelfEvolutionEngine
from engine.v7_autonomous_business_engine import V7AutonomousBusiness
from engine.v8_self_rewriting_company import V8SelfRewritingCompany

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


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V8 SELF REWRITING COMPANY ACTIVE"}


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
    return conversion.track_conversion(product_id, 50.0)


# =========================
# SCALING
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# V8 CORE LOOP
# =========================

@app.get("/v8/run")
def v8_run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return v8.run(products)


# =========================
# V8 COMPANY REPORT
# =========================

@app.get("/v8/report")
def v8_report():

    return v8.report()


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
        "v8": v8.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# SAFE AUTOPILOT ENTRY
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "v8")
    conversion.track_lead("CHK24_001", "v8")
    conversion.track_conversion("CHK24_001", 50.0)

    scale = scaling.analyze_product("CHK24_001")
    v8_state = v8.run(["CHK24_001", "TC_001", "AMZ_001"])

    return {
        "status": "V8_CYCLE_DONE",
        "scale": scale,
        "v8": v8_state
    }
