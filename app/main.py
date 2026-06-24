from fastapi import FastAPI, Request
from datetime import datetime

# =========================
# SAFE IMPORTS (NO CRASH MODE)
# =========================

try:
    from engine.tracking_engine import TrackingEngine
except:
    class TrackingEngine:
        def __init__(self):
            self.clicks = []
            self.conversions = []

        def track_click(self, product_id, source="api"):
            self.clicks.append({
                "product_id": product_id,
                "source": source,
                "timestamp": datetime.utcnow().isoformat()
            })
            return {"status": "CLICK_TRACKED"}

        def get_summary(self):
            return {
                "clicks": len(self.clicks),
                "conversions": len(self.conversions)
            }


try:
    from engine.traffic_engine import TrafficEngine
except:
    class TrafficEngine:
        def run_bulk_traffic(self, products):
            return {"status": "TRAFFIC_FALLBACK", "products": products}

        def get_stats(self):
            return {"traffic": 0}


# =========================
# CORE IMPORTS
# =========================

from engine.orchestrator_engine_v2 import run_orchestrator
from engine.master_content_pipeline import MasterContentPipeline
from engine.email_system import EmailMarketingEngine, add_email, get_all_emails
from engine.autopilot_connector import AutopilotConnector
from engine.governor import Governor
from engine.sales_api_engine import SalesAPIEngine


# =========================
# APP INIT
# =========================

app = FastAPI()

pipeline = MasterContentPipeline()
tracking = TrackingEngine()
traffic = TrafficEngine()

email_engine = EmailMarketingEngine(get_all_emails().get("emails", []))

# =========================
# SALES ENGINE (REAL MONEY LAYER)
# =========================

sales_engine = SalesAPIEngine()


# =========================
# CONNECTOR
# =========================

connector = AutopilotConnector(
    orchestrator=run_orchestrator,
    pipeline=pipeline,
    email_engine=email_engine,
    tracking=tracking
)

governor = Governor()


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "AUTOPILOT LIVE + SALES CONNECTED"
    }


# =========================
# HEALTH (CRITICAL)
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# ENGINE STATUS
# =========================

@app.get("/engine")
def engine():
    return {
        "status": "ACTIVE",
        "tracking": True,
        "traffic": True,
        "sales": True,
        "governor": True
    }


# =========================
# FLOW (MAIN MONEY FLOW)
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    decision = governor.approve(product_id, 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    # =========================
    # AUTOPILOT CORE
    # =========================
    result = connector.run_cycle(product_id, "check24")

    # =========================
    # TRACK CLICK
    # =========================
    tracking.track_click(product_id, source="flow")

    # =========================
    # REAL SALES API CONNECT
    # =========================
    sales_result = sales_engine.send_lead(
        product_id=product_id,
        source="flow"
    )

    return {
        "status": "FLOW_COMPLETE",
        "timestamp": datetime.utcnow().isoformat(),
        "autopilot": result,
        "sales": sales_result
    }


# =========================
# RUN
# =========================

@app.get("/run")
def run():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    sales_engine.send_lead("CHK24_001", "run")

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# AUTOPILOT
# =========================

@app.get("/autopilot")
def autopilot():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    sales_engine.send_lead("CHK24_001", "autopilot")

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# LOOP
# =========================

@app.get("/loop")
def loop():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    sales_engine.send_lead("CHK24_001", "loop")

    return {
        "traffic": traffic.run_bulk_traffic([
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]),
        "autopilot": connector.run_cycle("CHK24_001", "check24")
    }


# =========================
# TRAFFIC
# =========================

@app.get("/traffic")
def generate_traffic():
    return traffic.run_bulk_traffic([
        "CHK24_001",
        "TC_001",
        "AMZ_001"
    ])


# =========================
# TRACK CLICK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return tracking.track_click(
        data.get("product_id"),
        data.get("source", "api")
    )


# =========================
# SALES STATUS
# =========================

@app.get("/sales")
def sales():

    return sales_engine.get_sales_stats()


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
        "sales": sales_engine.get_sales_stats(),
        "governor": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
