from fastapi import FastAPI
from datetime import datetime

from engine.conversion_engine_v3 import ConversionTrackingV3
from engine.scaling_engine_v4 import ScalingEngineV4

app = FastAPI()

# =========================
# INIT SYSTEM
# =========================

conversion = ConversionTrackingV3()
scaling = ScalingEngineV4(conversion)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "SCALING ENGINE V4 ACTIVE"}


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
# CONVERT (REVENUE EVENT)
# =========================

@app.get("/convert/{product_id}")
def convert(product_id: str):
    return conversion.track_conversion(product_id, 15.0)


# =========================
# SCORE
# =========================

@app.get("/score/{product_id}")
def score(product_id: str):
    return conversion.product_score(product_id)


# =========================
# SCALING DECISION (CORE V4)
# =========================

@app.get("/scale/{product_id}")
def scale(product_id: str):
    return scaling.analyze_product(product_id)


# =========================
# FULL SYSTEM SCAN
# =========================

@app.get("/scan")
def scan():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return scaling.scan_all(products)


# =========================
# DASHBOARD (FULL INTELLIGENCE)
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "conversion": conversion.report(),
        "scaling": scaling.report(),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# AUTOPILOT SIMULATION
# =========================

@app.get("/run")
def run():

    conversion.track_click("CHK24_001", "autopilot")
    conversion.track_lead("CHK24_001", "sales")
    conversion.track_conversion("CHK24_001", 25.0)

    scale_result = scaling.analyze_product("CHK24_001")

    return {
        "status": "V4_CYCLE_DONE",
        "conversion": conversion.product_score("CHK24_001"),
        "scaling": scale_result
    }
