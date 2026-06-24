from fastapi import FastAPI, Request

# =========================
# ENGINE IMPORTS
# =========================
from engine.orchestrator_engine_v2 import run_orchestrator
from engine.master_content_pipeline import MasterContentPipeline
from engine.email_system import EmailMarketingEngine, add_email, get_all_emails
from engine.revenue_autopilot_engine import RevenueAutopilotEngine
from engine.tracking_engine import TrackingEngine
from engine.traffic_engine import TrafficEngine
from engine.autopilot_connector import AutopilotConnector


# =========================
# APP INIT
# =========================
app = FastAPI()


# =========================
# SYSTEM INIT
# =========================
pipeline = MasterContentPipeline()

tracking = TrackingEngine()

traffic = TrafficEngine()

revenue_engine = RevenueAutopilotEngine(tracking)

email_engine = EmailMarketingEngine(get_all_emails().get("emails", []))


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
        "system": "FULL MONEY AUTOPILOT LIVE 🚀"
    }


# =========================
# TRAFFIC GENERATION
# =========================
@app.get("/traffic")
def generate_traffic():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    result = traffic.run_bulk_traffic(products)

    return result


# =========================
# TRACK CLICK
# =========================
@app.post("/track")
async def track(request: Request):

    data = await request.json()

    return tracking.track_click(
        product_id=data.get("product_id"),
        source=data.get("source", "api")
    )


# =========================
# EMAIL SIGNUP
# =========================
@app.post("/subscribe")
async def subscribe(request: Request):

    data = await request.json()

    email = data.get("email")

    return add_email(email)


# =========================
# AUTOPILOT CORE
# =========================
@app.get("/autopilot")
def autopilot():

    return connector.run_cycle(
        product_id="CHK24_001",
        category="check24"
    )


# =========================
# FULL LOOP (TRAFFIC → MONEY)
# =========================
@app.get("/loop")
def loop():

    traffic_result = traffic.run_bulk_traffic([
        "CHK24_001",
        "TC_001",
        "AMZ_001"
    ])

    autopilot_result = connector.run_cycle("CHK24_001", "check24")

    return {
        "status": "FULL_LOOP_DONE",
        "traffic": traffic_result,
        "autopilot": autopilot_result
    }


# =========================
# DASHBOARD (REAL MONEY VIEW)
# =========================
@app.get("/dashboard")
def dashboard():

    return {
        "traffic": traffic.get_stats(),
        "revenue": revenue_engine.run_cycle(),
        "tracking": tracking.get_summary(),
        "emails": get_all_emails()
    }


# =========================
# ENGINE STATUS
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "FULL SYSTEM ACTIVE",
        "traffic": True,
        "autopilot": True,
        "email": True,
        "tracking": True,
        "revenue": True
    }
