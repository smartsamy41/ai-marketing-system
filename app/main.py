from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# =========================
# CORE TRACKING
# =========================

class Tracking:
    def __init__(self):
        self.clicks = 0

    def track(self):
        self.clicks += 1
        return self.clicks

tracking = Tracking()

# =========================
# SIMPLE REVENUE SIMULATION
# =========================

class Revenue:
    def __init__(self):
        self.value = 0

    def add(self, amount=5):
        self.value += amount
        return self.value

revenue = Revenue()

# =========================
# AUTONOMY LOOP IMPORT
# =========================

from engine.v5_autonomy_loop import AutonomyLoopV5

autonomy = AutonomyLoopV5()

# =========================
# LANDINGPAGE
# =========================

class Landingpage:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "status": "CREATED"
        }

landingpage = Landingpage()

# =========================
# PROCESS FLOW
# =========================

def process(product_id):

    landingpage.create(product_id)
    tracking.track()

    revenue.add(5)

    autonomy.collect(
        traffic=1,
        clicks=1,
        leads=1,
        revenue=5
    )

    return {
        "product_id": product_id,
        "clicks": tracking.clicks,
        "revenue": revenue.value
    }

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "V5 AUTONOMY ACTIVE"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RUN LOOP (AUTONOMY CORE)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:
        results.append(process(p))

    decision = autonomy.decide()

    return {
        "status": "RUN_OK",
        "results": results,
        "autonomy": decision,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# DECISION ONLY
# =========================

@app.get("/decide")
def decide():
    return autonomy.decide()

# =========================
# RESET LOOP
# =========================

@app.get("/reset")
def reset():
    return autonomy.reset()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.clicks,
        "revenue": revenue.value,
        "decision": autonomy.decide(),
        "system": "AUTONOMY LOOP V5",
        "timestamp": datetime.utcnow().isoformat()
    }
