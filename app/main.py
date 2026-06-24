from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# SIMPLE TRACKING (STABLE CORE)
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
# LANDINGPAGE (SAFE SIMPLE VERSION)
# =========================

class LandingpageEngine:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "url": f"/landing/{product_id}",
            "status": "CREATED",
            "timestamp": datetime.utcnow().isoformat()
        }


landingpage = LandingpageEngine()

# =========================
# SALES API (PLACEHOLDER READY)
# =========================

class SalesAPI:
    def send(self, product_id):
        return {
            "product_id": product_id,
            "status": "SENT_TO_SALES_API",
            "timestamp": datetime.utcnow().isoformat()
        }


sales = SalesAPI()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "CLEAN MARKETING SYSTEM ACTIVE"}

# =========================
# HEALTH (CLOUD SAFE)
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# FLOW (MAIN MONEY FLOW)
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    lp = landingpage.create(product_id)
    click = tracking.track(product_id, "flow")
    sales_event = sales.send(product_id)

    return {
        "status": "FLOW_COMPLETE",
        "landingpage": lp,
        "tracking": click,
        "sales": sales_event
    }

# =========================
# PINTEREST QUEUE (NUR PREP, KEIN ADS CODE)
# =========================

@app.get("/pin/{product_id}")
def pin(product_id: str):

    return {
        "product_id": product_id,
        "pin_status": "READY_FOR_PINTEREST",
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.summary(),
        "system": "STABLE READY",
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# RUN (CLOUD SAFE ENTRY)
# =========================

@app.get("/run")
def run():

    product_id = "CHK24_001"

    lp = landingpage.create(product_id)
    tracking.track(product_id, "run")
    sales.send(product_id)

    return {
        "status": "RUN_COMPLETE",
        "landingpage": lp,
        "tracking": tracking.summary()
    }
