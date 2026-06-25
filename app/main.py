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
        event = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.clicks.append(event)
        return {"status": "CLICK_TRACKED", "event": event}

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
            "description": f"Beste Angebote für {product_id}. Jetzt vergleichen.",
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

landingpage_engine = LandingpageEngine()

# =========================
# SALES ENGINE (SAFE)
# =========================

class SalesAPIEngine:
    def send_lead(self, product_id, source="api"):
        return {
            "product_id": product_id,
            "source": source,
            "status": "SENT"
        }

sales_engine = SalesAPIEngine()

# =========================
# REVENUE VERIFICATION V2
# =========================

class RevenueVerificationV2:

    def __init__(self):
        self.leads = []

    def send_lead(self, product_id, source="api"):

        lead = {
            "product_id": product_id,
            "source": source,
            "status": "SENT",
            "revenue": 0,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.leads.append(lead)
        return lead

    def update_from_sales(self, product_id, status, revenue=0):

        for lead in self.leads:
            if lead["product_id"] == product_id:
                lead["status"] = status
                lead["revenue"] = revenue
                lead["updated_at"] = datetime.utcnow().isoformat()
                return lead

        return {"status": "NOT_FOUND"}

    def analytics(self):

        total = len(self.leads)
        confirmed = len([l for l in self.leads if l["status"] == "CONFIRMED"])
        rejected = len([l for l in self.leads if l["status"] == "REJECTED"])
        revenue = sum([l["revenue"] for l in self.leads])

        return {
            "total_leads": total,
            "confirmed": confirmed,
            "rejected": rejected,
            "revenue": revenue,
            "conversion_rate": (confirmed / total) if total > 0 else 0
        }

revenue = RevenueVerificationV2()

# =========================
# CORE PROCESS
# =========================

def process_product(product_id):

    lp = landingpage_engine.create(product_id)

    tracking.track_click(product_id, "flow")

    sales_engine.send_lead(product_id)

    revenue.send_lead(product_id)

    return {
        "landingpage": lp,
        "tracking": tracking.get_summary(),
        "sales": sales_engine.send_lead(product_id),
        "revenue": revenue.analytics()
    }

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "MAIN V4 FULL FINAL"
    }

# =========================
# HEALTH (CLOUD SAFE)
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
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
        "revenue": revenue.analytics(),
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):
    return process_product(product_id)

# =========================
# SALES STATUS
# =========================

@app.get("/sales")
def sales():
    return {"status": "ACTIVE"}

# =========================
# REVENUE DASHBOARD
# =========================

@app.get("/revenue")
def revenue_status():
    return revenue.analytics()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "tracking": tracking.get_summary(),
        "revenue": revenue.analytics(),
        "system": "STABLE V4 FULL",
        "timestamp": datetime.utcnow().isoformat()
    }
