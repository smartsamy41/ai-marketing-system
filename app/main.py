from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# TRACKING
# =========================

class TrackingEngine:
    def __init__(self):
        self.clicks = []

    def track_click(self, product_id, source="api"):
        self.clicks.append({
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {"status": "CLICK_TRACKED"}

    def get_summary(self):
        return {"clicks": len(self.clicks)}

tracking = TrackingEngine()

# =========================
# LANDINGPAGE ENGINE
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

landingpage_engine = LandingpageEngine()

# =========================
# SALES API (SAFE MOCK / READY FOR CONNECT)
# =========================

class SalesAPIEngine:
    def send_lead(self, product_id, source="api"):
        return {
            "product_id": product_id,
            "source": source,
            "status": "SENT_TO_SALES_API"
        }

sales_engine = SalesAPIEngine()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "CLEAN MAIN FINAL"
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
# CORE FLOW
# =========================

def process_product(product_id: str):

    landingpage = landingpage_engine.create(product_id)
    tracking.track_click(product_id, "flow")
    sales = sales_engine.send_lead(product_id, "flow")

    return {
        "landingpage": landingpage,
        "tracking": tracking.get_summary(),
        "sales": sales
    }

# =========================
# RUN PIPELINE
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
# SINGLE FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):
    return process_product(product_id)

# =========================
# TRAFFIC SIM (OPTIONAL)
# =========================

@app.get("/traffic")
def traffic():
    return {
        "status": "OK",
        "message": "traffic layer ready"
    }

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "tracking": tracking.get_summary(),
        "system": "STABLE PRODUCTION",
        "timestamp": datetime.utcnow().isoformat()
    }
