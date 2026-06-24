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
            click = {
                "product_id": product_id,
                "source": source,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.clicks.append(click)
            return {"status": "CLICK_TRACKED", "click": click}

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

# 🔥 FIX: revenue_engine MUSS existieren
revenue_engine = RevenueAutopilotEngine(tracking)

email_engine = EmailMarketingEngine(get_all_emails().get("emails", []))

# 🔥 FIX: revenue_engine korrekt übergeben
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
    return {
        "status": "OK",
        "system": "AUTOPILOT LIVE"
    }


# =========================
# HEALTH (CLOUD RUN CRITICAL)
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
        "revenue": True,
        "governor": True
    }


# =========================
# GOVERNOR CHECK
# =========================

def check_governor(product_id="CHK24_001", traffic_amount=5, score=0.8):
    return governor.approve(product_id, traffic_amount, score)


# =========================
# RUN FLOW
# =========================

@app.get("/run")
def run():

    decision = check_governor()

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# AUTOPILOT
# =========================

@app.get("/autopilot")
def autopilot():

    decision = check_governor()

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

    return connector.run_cycle("CHK24_001", "check24")


# =========================
# LOOP TEST
# =========================

@app.get("/loop")
def loop():

    decision = check_governor()

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED", "reason": decision}

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
        product_id=data.get("product_id"),
        source=data.get("source", "api")
    )


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
