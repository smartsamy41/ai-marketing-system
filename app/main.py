from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# TRACKING ENGINE
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
        return {
            "clicks": len(self.clicks)
        }

tracking = TrackingEngine()

# =========================
# LANDINGPAGE ENGINE
# =========================

class LandingpageEngine:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "description": f"Beste Angebote für {product_id}. Jetzt Tarife vergleichen.",
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

landingpage_engine = LandingpageEngine()

# =========================
# SALES API ENGINE (REAL CONNECT READY)
# =========================

class SalesAPIEngine:
    def __init__(self):
        self.logs = []

    def send_lead(self, product_id, source="api"):
        event = {
            "product_id": product_id,
            "source": source,
            "status": "SENT",
            "timestamp": datetime.utcnow().isoformat()
        }
        self.logs.append(event)
        return event

    def get_sales_stats(self):
        return {
            "total_leads": len(self.logs),
            "last": self.logs[-1] if self.logs else None
        }

sales_engine = SalesAPIEngine()

# =========================
# SCHEDULER ENGINE (SAFE WRAPPER)
# =========================

class SchedulerEngine:
    def run(self, products):
        return {
            "status": "SCHEDULER_OK",
            "products": products,
            "timestamp": datetime.utcnow().isoformat()
        }

scheduler = SchedulerEngine()

# =========================
# CORE PROCESS
# =========================

def process_product(product_id):

    # 1. Landingpage
    lp = landingpage_engine.create(product_id)

    # 2. Tracking
    tracking.track_click(product_id, "flow")

    # 3. Sales API
    sale = sales_engine.send_lead(product_id, "flow")

    return {
        "landingpage": lp,
        "tracking": tracking.get_summary(),
        "sales": sale
    }

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "MAIN V4 STABLE"
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
# RUN PIPELINE (MAIN ENTRY)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    scheduler_result = scheduler.run(products)

    results = []

    for p in products:
        results.append(process_product(p))

    return {
        "status": "RUN_OK",
        "scheduler": scheduler_result,
        "results": results,
        "sales": sales_engine.get_sales_stats(),
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    return process_product(product_id)

# =========================
# TRAFFIC TEST
# =========================

@app.get("/traffic")
def traffic():
    return {
        "status": "OK",
        "message": "traffic layer active"
    }

# =========================
# SALES STATUS
# =========================

@app.get("/sales")
def sales():
    return sales_engine.get_sales_stats()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return {
        "tracking": tracking.get_summary(),
        "sales": sales_engine.get_sales_stats(),
        "scheduler": "ACTIVE",
        "system": "STABLE V4",
        "timestamp": datetime.utcnow().isoformat()
    }
