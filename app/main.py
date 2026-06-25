from fastapi import FastAPI
from datetime import datetime

from engine.api_connector import APIConnector

app = FastAPI()

# =========================
# CORE
# =========================

class Tracking:
    def track(self, product_id):
        return {"product_id": product_id, "status": "TRACKED"}

class Landingpage:
    def create(self, product_id):
        return {
            "product_id": product_id,
            "url": f"/landing/{product_id}",
            "status": "CREATED"
        }

tracking = Tracking()
landingpage = Landingpage()
api = APIConnector()

# =========================
# ORCHESTRATOR
# =========================

class Orchestrator:

    def run(self, product_id):

        lp = landingpage.create(product_id)
        track = tracking.track(product_id)

        sales = api.send_sales_lead(product_id)

        youtube = api.upload_youtube_video(
            title=f"{product_id} Vergleich 2026",
            description="Auto Content"
        )

        pinterest = api.create_pinterest_pin(
            title=f"{product_id} sparen & vergleichen"
        )

        return {
            "product_id": product_id,
            "landingpage": lp,
            "tracking": track,
            "sales": sales,
            "youtube": youtube,
            "pinterest": pinterest
        }

orchestrator = Orchestrator()

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "MINIMAL LIVE V1"}

@app.get("/health")
def health():
    return {"status": "OK", "ready": True}

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return {
        "status": "RUNNING",
        "results": [orchestrator.run(p) for p in products],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/flow/{product_id}")
def flow(product_id: str):
    return orchestrator.run(product_id)

@app.get("/report")
def report():
    return api.report()
