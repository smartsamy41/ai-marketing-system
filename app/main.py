from fastapi import FastAPI, Request
from datetime import datetime

from engine.tracking_engine import TrackingEngine
from engine.traffic_engine import TrafficEngine
from engine.orchestrator_engine_v2 import run_orchestrator
from engine.master_content_pipeline import MasterContentPipeline
from engine.email_system import EmailMarketingEngine, add_email, get_all_emails
from engine.revenue_autopilot_engine import RevenueAutopilotEngine
from engine.autopilot_connector import AutopilotConnector
from engine.governor import Governor


# =========================
# APP INIT
# =========================

app = FastAPI()

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

governor = Governor()


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "AUTOPILOT LIVE"}


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


# =========================
# ENGINE STATUS
# =========================

@app.get("/engine")
def engine():
    return {
        "status": "ACTIVE",
        "tracking": True,
        "traffic": True,
        "revenue": True,
        "governor": True
    }


# =========================
# RUN (SCHEDULER SAFE)
# =========================

@app.get("/run")
def run():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# AUTOPILOT
# =========================

@app.get("/autopilot")
def autopilot():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# LOOP
# =========================

@app.get("/loop")
def loop():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    return {
        "traffic": traffic.run_bulk_traffic(["CHK24_001", "TC_001", "AMZ_001"]),
        "autopilot": connector.run_cycle("CHK24_001", "check24")
    }


# =========================
# TRAFFIC
# =========================

@app.get("/traffic")
def generate_traffic():
    return traffic.run_bulk_traffic(["CHK24_001", "TC_001", "AMZ_001"])


# =========================
# TRACK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return tracking.track_click(data.get("product_id"), data.get("source", "api"))


# =========================
# EMAIL
# =========================

@app.post("/subscribe")
async def subscribe(request: Request):
    data = await request.json()
    return add_email(data.get("email"))


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "traffic": traffic.get_stats(),
        "tracking": tracking.get_summary(),
        "revenue": revenue_engine.run_cycle(),
        "emails": get_all_emails(),
        "governor": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
