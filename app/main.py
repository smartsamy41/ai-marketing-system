from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# =========================
# CORE SERVICES
# =========================

class Tracking:
    def track_click(self, product_id, source="api"):
        return {"product_id": product_id, "status": "tracked"}

class Landingpage:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

class Sales:
    def send_lead(self, product_id, source="api"):
        return {"product_id": product_id, "status": "SENT"}

tracking = Tracking()
landingpage = Landingpage()
sales = Sales()

# =========================
# ORCHESTRATOR
# =========================

class Orchestrator:

    def run(self, product_id):

        lp = landingpage.create(product_id)
        tracking.track_click(product_id)
        sales.send_lead(product_id)

        return {
            "product_id": product_id,
            "landingpage": lp,
            "youtube": {
                "title": f"{product_id} Vergleich 2026",
                "status": "READY"
            },
            "pinterest": {
                "pin_title": f"{product_id} sparen & vergleichen",
                "status": "READY"
            }
        }

orchestrator = Orchestrator()

# =========================
# LIVE POSTING ENGINE
# =========================

from engine.live_posting_activation_v1 import LivePostingActivationV1

publisher = LivePostingActivationV1()

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE POSTING ACTIVATION V1"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RUN FULL PIPELINE
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    processed = []

    for p in products:
        result = orchestrator.run(p)
        posted = publisher.post_product(result)

        processed.append({
            "orchestrator": result,
            "live_posting": posted
        })

    return {
        "status": "LIVE_POSTING_RUNNING",
        "results": processed,
        "report": publisher.report(),
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE FLOW
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    result = orchestrator.run(product_id)
    posted = publisher.post_product(result)

    return {
        "orchestrator": result,
        "live_posting": posted
    }

# =========================
# REPORT
# =========================

@app.get("/report")
def report():
    return publisher.report()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "posting_report": publisher.report(),
        "system": "LIVE CONTENT PIPELINE ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
