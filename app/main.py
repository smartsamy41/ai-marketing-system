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
# ORCHESTRATOR (MINIMAL)
# =========================

class Orchestrator:

    def run(self, product_id):

        lp = landingpage.create(product_id)
        tracking.track_click(product_id)
        sales.send_lead(product_id)

        return {
            "product_id": product_id,
            "landingpage": lp
        }

orchestrator = Orchestrator()

# =========================
# CONTENT ACTIVATION ENGINE
# =========================

from engine.real_content_activation_v1 import RealContentActivationV1

content_engine = RealContentActivationV1(orchestrator)

# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "REAL CONTENT ACTIVATION V1"}

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

# =========================
# RUN (FULL CONTENT GENERATION)
# =========================

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    result = content_engine.run_batch(products)

    return {
        "status": "CONTENT_GENERATED",
        "results": result,
        "report": content_engine.report(),
        "timestamp": datetime.utcnow().isoformat()
    }

# =========================
# SINGLE PRODUCT
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    return content_engine.run_product(product_id)

# =========================
# REPORT
# =========================

@app.get("/report")
def report():
    return content_engine.report()

# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "report": content_engine.report(),
        "system": "LIVE CONTENT PIPELINE ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }
