from fastapi import FastAPI

# =========================
# ENGINE IMPORTS
# =========================
from engine.autopilot_connector import AutopilotConnector

from engine.orchestrator_engine_v2 import run_orchestrator
from engine.master_content_pipeline import MasterContentPipeline
from engine.email_system import EmailMarketingEngine
from engine.tracking_engine import TrackingEngine
from engine.revenue_autopilot_engine import RevenueAutopilotEngine


# =========================
# APP INIT
# =========================
app = FastAPI()


# =========================
# INIT SYSTEMS
# =========================
pipeline = MasterContentPipeline()

tracking = TrackingEngine()

revenue_engine = RevenueAutopilotEngine(tracking)

email_engine = EmailMarketingEngine([])

connector = AutopilotConnector(
    orchestrator=run_orchestrator,
    pipeline=pipeline,
    email_engine=email_engine,
    tracking=tracking,
    revenue_engine=revenue_engine
)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "AUTOPILOT LIVE"
    }


# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "system_ready": True
    }


# =========================
# AUTOPILOT RUN (SINGLE CYCLE)
# =========================
@app.get("/autopilot")
def autopilot():

    result = connector.run_cycle(
        product_id="CHK24_001",
        category="check24"
    )

    return result


# =========================
# CONTINUOUS LOOP SIMULATION
# =========================
@app.get("/loop")
def loop():

    results = []

    products = [
        ("CHK24_001", "check24"),
        ("TC_001", "tarifcheck"),
        ("AMZ_001", "amazon")
    ]

    for product_id, category in products:

        results.append(
            connector.run_cycle(product_id, category)
        )

    return {
        "status": "LOOP_DONE",
        "cycles": len(results),
        "results": results
    }


# =========================
# TRACKING ENDPOINT
# =========================
@app.post("/track")
async def track(request):

    data = await request.json()

    return tracking.track_click(
        product_id=data.get("product_id"),
        source="api"
    )


# =========================
# REVENUE DASHBOARD
# =========================
@app.get("/dashboard")
def dashboard():

    return revenue_engine.run_cycle()
