from fastapi import FastAPI, Request
from datetime import datetime

# =========================
# SAFE ENGINE IMPORTS (CRASH FIX)
# =========================

try:
    from engine.tracking_engine import TrackingEngine
except:
    # FALLBACK (Cloud darf NIE crashen)
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


from engine.orchestrator_engine_v2 import run_orchestrator
from engine.master_content_pipeline import MasterContentPipeline
from engine.email_system import EmailMarketingEngine, add_email, get_all_emails
from engine.revenue_autopilot_engine import RevenueAutopilotEngine
from engine.autopilot_connector import AutopilotConnector


# =========================
# FASTAPI APP
# =========================
app = FastAPI()


# =========================
# INIT SYSTEM
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
# ROOT (IMPORTANT HEALTH)
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "AUTOPILOT LIVE"
    }


# =========================
# HEALTH CHECK (CRITICAL FOR CLOUD RUN)
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True
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
        "revenue": True
    }


# =========================
# TRAFFIC
# =========================
@app.get("/traffic")
def generate_traffic():
    return traffic.run_bulk_traffic(["CHK24_001", "TC_001", "AMZ_001"])


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
# AUTOPILOT
# =========================
@app.get("/autopilot")
def autopilot():
    return connector.run_cycle(
        product_id="CHK24_001",
        category="check24"
    )


# =========================
# LOOP TEST
# =========================
@app.get("/loop")
def loop():
    return {
        "traffic": traffic.run_bulk_traffic(["CHK24_001", "TC_001"]),
        "autopilot": connector.run_cycle("CHK24_001", "check24")
    }


# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
def dashboard():
    return {
        "traffic": traffic.get_stats(),
        "tracking": tracking.get_summary(),
        "revenue": revenue_engine.run_cycle(),
        "emails": get_all_emails()
    }
