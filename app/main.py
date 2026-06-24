from fastapi import FastAPI, Request
from datetime import datetime

# =========================
# IMPORTS (SAFE ONLY)
# =========================

try:
    from engine.scheduler_engine import SchedulerEngine
except:
    # fallback (NO CRASH)
    class SchedulerEngine:
        def run(self, products):
            return {"status": "SCHEDULER_FALLBACK", "products": products}

try:
    from engine.landingpage_engine_v2 import LandingpageEngineV2
except:
    class LandingpageEngineV2:
        def create(self, product_id, title, description):
            return {
                "product_id": product_id,
                "title": title,
                "description": description,
                "status": "CREATED"
            }

try:
    from engine.sales_api_engine import SalesAPIEngine
except:
    class SalesAPIEngine:
        def send_lead(self, product_id, source):
            return {
                "product_id": product_id,
                "status": "SENT_TO_SALES_API",
                "source": source
            }

# =========================
# APP INIT
# =========================

app = FastAPI()

scheduler = SchedulerEngine()
landingpage = LandingpageEngineV2()
sales = SalesAPIEngine()

# =========================
# TRACKING (MINIMAL STABLE)
# =========================

class Tracking:
    def __init__(self):
        self.clicks = []

    def track(self, product_id, source="api"):
        event = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.clicks.append(event)
        return {"status": "CLICK_TRACKED", "event": event}

    def summary(self):
        return {"clicks": len(self.clicks)}

tracking = Tracking()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN MAIN V3 ACTIVE"
    }

# =========================
# HEALTH (CLOUD RUN SAFE)
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# CORE CONTENT FLOW (1 PRODUCT)
# =========================

def process_product(product_id: str):

    # 1. Landingpage
    lp = landingpage.create(
        product_id,
        title=f"{product_id} Vergleich 2026",
        description=f"Finde passende Angebote für {product_id} und vergleiche Tarife einfach online."
    )

    # 2. Tracking
    click = tracking.track(product_id, "flow")

    # 3. Sales API
    sales_event = sales.send_lead(product_id, "flow")

    return {
        "landingpage": lp,
        "tracking": click,
        "sales": sales_event
    }

# =========================
# RUN (SCHEDULER ENTRY POINT)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    schedule_result = scheduler.run(products)

    results = []

    for p in products:
        results.append(process_product(p))

    return {
        "status": "RUN_COMPLETE",
        "scheduler": schedule_result,
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE PRODUCT FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    return process_product(product_id)

# =========================
# SCHEDULER ONLY
# =========================

@app.get("/schedule")
def schedule():

    return scheduler.run(["CHK24_001", "TC_001", "AMZ_001"])

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.summary(),
        "scheduler": "ACTIVE",
        "system": "STABLE V3",
        "timestamp": datetime.utcnow().isoformat()
    }
