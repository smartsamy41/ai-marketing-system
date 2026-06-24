from fastapi import FastAPI, Request
from datetime import datetime

# =========================
# SAFE IMPORTS
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
from engine.landingpage_engine import LandingpageEngine
from engine.affiliate_router import AffiliateRouter


# =========================
# APP INIT
# =========================

app = FastAPI()

pipeline = MasterContentPipeline()
tracking = TrackingEngine()
traffic = TrafficEngine()

email_engine = EmailMarketingEngine(get_all_emails().get("emails", []))

connector = AutopilotConnector(
    orchestrator=run_orchestrator,
    pipeline=pipeline,
    email_engine=email_engine,
    tracking=tracking
)

governor = Governor()
landingpage_engine = LandingpageEngine()
affiliate_router = AffiliateRouter()


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
# ENGINE
# =========================

@app.get("/engine")
def engine():
    return {
        "status": "ACTIVE",
        "tracking": True,
        "traffic": True,
        "governor": True,
        "flow": True
    }


# =========================
# FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    products = {
        "CHK24_001": "Strom Vergleich",
        "TC_001": "Solar Vergleich",
        "AMZ_001": "Amazon Produkt"
    }

    product_name = products.get(product_id, "Unknown Product")

    decision = governor.approve(product_id, 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    existing = landingpage_engine.get(product_id)

    if existing.get("status") == "NOT_FOUND":
        lp = landingpage_engine.create(product_id, product_name, "general")
    else:
        lp = existing

    affiliate = affiliate_router.get_redirect(product_id)

    tracking.track_click(product_id, source="flow")

    return {
        "status": "FLOW_COMPLETE",
        "timestamp": datetime.utcnow().isoformat(),
        "landingpage": lp,
        "affiliate": affiliate
    }


# =========================
# RUN
# =========================

@app.get("/run")
def run():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# AUTOPILOT
# =========================

@app.get("/autopilot")
def autopilot():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# LOOP
# =========================

@app.get("/loop")
def loop():

    decision = governor.approve("CHK24_001", 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

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
        "governor": "ACTIVE",
        "flow": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
