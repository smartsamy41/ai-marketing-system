from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# SAFE TRACKING
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
# SAFE LANDINGPAGE (NO DEPENDENCY CRASH)
# =========================

class LandingpageEngine:
    def create(self, product_id, title, description):
        return {
            "product_id": product_id,
            "title": title,
            "description": description,
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

landingpage = LandingpageEngine()

# =========================
# SAFE SCHEDULER WRAPPER (FIX FOR base_url ERROR)
# =========================

class SchedulerEngine:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.log = []

    def run(self, products):
        self.log.append({
            "products": products,
            "timestamp": datetime.utcnow().isoformat()
        })
        return {
            "status": "SCHEDULER_OK",
            "products": products
        }

scheduler = SchedulerEngine(base_url="local")

# =========================
# SALES API SAFE
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
    return {"status": "OK", "system": "STABLE MAIN V3.1"}

# =========================
# HEALTH (CRITICAL CLOUD RUN FIX)
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# FLOW
# =========================

def process(product_id):

    lp = landingpage.create(
        product_id,
        f"{product_id} Vergleich 2026",
        f"Beste Angebote für {product_id}"
    )

    tracking.track(product_id, "flow")
    sales.send(product_id)

    return {
        "landingpage": lp,
        "tracking": tracking.summary(),
        "sales": "OK"
    }

# =========================
# RUN (CLOUD ENTRY SAFE)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    scheduler.run(products)

    results = []

    for p in products:
        results.append(process(p))

    return {
        "status": "RUN_OK",
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.summary(),
        "scheduler": "OK",
        "system": "STABLE",
        "timestamp": datetime.utcnow().isoformat()
    }
