from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# CORE TRACKING
# =========================

class TrackingEngine:
    def __init__(self):
        self.clicks = 0

    def track(self):
        self.clicks += 1
        return {"clicks": self.clicks}

tracking = TrackingEngine()

# =========================
# SCALE SYSTEM IMPORT
# =========================

from engine.scale_system_v1 import ScaleSystemV1

scale_engine = ScaleSystemV1()

# =========================
# LANDINGPAGE
# =========================

class LandingpageEngine:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "status": "CREATED"
        }

landingpage = LandingpageEngine()

# =========================
# REVENUE SIM (CONNECTED LATER)
# =========================

class Revenue:
    def __init__(self):
        self.revenue = 0

    def add(self, value=5):
        self.revenue += value
        return self.revenue

revenue = Revenue()

# =========================
# FLOW
# =========================

def process(product_id):

    landingpage.create(product_id)
    tracking.track()

    revenue.add(5)

    scale_engine.update(
        traffic=1,
        clicks=1,
        leads=1,
        revenue=5
    )

    return {
        "product_id": product_id,
        "landingpage": "OK",
        "tracking": tracking.clicks,
        "revenue": revenue.revenue
    }

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "SCALE V1 ACTIVE"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RUN (MAIN ENTRY)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:
        results.append(process(p))

    decision = scale_engine.decision()

    return {
        "status": "RUN_OK",
        "results": results,
        "scale": decision,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SCALE DECISION ONLY
# =========================

@app.get("/scale")
def scale():

    return scale_engine.decision()

# =========================
# RESET SCALE CYCLE
# =========================

@app.get("/reset")
def reset():

    return scale_engine.reset()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "scale": scale_engine.decision(),
        "tracking": tracking.clicks,
        "revenue": revenue.revenue,
        "system": "SCALING ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
