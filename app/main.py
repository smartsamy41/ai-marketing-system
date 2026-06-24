from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# SAFETY LAYER (NO CRASH)
# =========================

class Tracking:
    def __init__(self):
        self.clicks = []

    def track(self, product_id, source="api"):
        self.clicks.append({
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {"status": "CLICK_TRACKED"}

    def summary(self):
        return {"clicks": len(self.clicks)}


tracking = Tracking()

# =========================
# LANDINGPAGE (CLEAN ONLY)
# =========================

class LandingpageEngine:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "description": f"Beste Angebote für {product_id}",
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }


landingpage = LandingpageEngine()

# =========================
# SALES API (SAFE MOCK / CONNECTOR READY)
# =========================

class SalesAPI:
    def send(self, product_id):
        return {
            "product_id": product_id,
            "status": "SENT_TO_SALES_API"
        }


sales = SalesAPI()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN MAIN FIX V1"
    }

# =========================
# HEALTH (CRITICAL FOR CLOUD RUN)
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SAFE PROCESS FLOW
# =========================

def process_product(product_id: str):

    lp = landingpage.create(product_id)
    click = tracking.track(product_id, "flow")
    sale = sales.send(product_id)

    return {
        "landingpage": lp,
        "tracking": click,
        "sales": sale
    }

# =========================
# RUN (SCHEDULER ENTRY POINT)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    results = []

    for p in products:
        results.append(process_product(p))

    return {
        "status": "RUN_OK",
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE FLOW TEST
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    return process_product(product_id)

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.summary(),
        "system": "STABLE",
        "timestamp": datetime.utcnow().isoformat()
    }
