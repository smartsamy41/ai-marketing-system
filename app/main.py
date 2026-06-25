from fastapi import FastAPI
from datetime import datetime

from engine.api_connector import APIConnector
from compliance_engine import ComplianceEngine
from profit_engine import ProfitEngine

app = FastAPI()

# =========================
# CORE MODULES
# =========================

api = APIConnector()
compliance_engine = ComplianceEngine()

# Profit Engine bekommt alle Systeme
profit_engine = ProfitEngine(
    sales_engine=api,
    compliance_engine=compliance_engine,
    commission_engine=compliance_engine
)

# =========================
# LANDING + TRACKING (SIMPLE CORE)
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

# =========================
# ORCHESTRATOR (OLD FLOW + PROFIT ENGINE)
# =========================

class Orchestrator:

    def run(self, product_id):

        # 1. CORE DATA
        lp = landingpage.create(product_id)
        track = tracking.track(product_id)

        # 2. PROFIT ENGINE (FULL SYSTEM)
        profit_data = profit_engine.process_product(product_id)

        # 3. OUTPUT CONTENT (PLACEHOLDER)
        youtube = api.upload_youtube_video(
            title=f"{product_id} Vergleich 2026",
            description="Auto Content"
        )

        pinterest = api.create_pinterest_pin(
            title=f"{product_id} sparen & vergleichen"
        )

        # 4. CONTENT COMPLIANCE CHECK (optional hook)
        compliance = compliance_engine.audit(
            content=str(profit_data),
            product={"source": "tarifcheck"}
        )

        return {
            "product_id": product_id,
            "landingpage": lp,
            "tracking": track,
            "profit": profit_data,
            "compliance": compliance,
            "youtube": youtube,
            "pinterest": pinterest
        }

orchestrator = Orchestrator()

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "FULL PROFIT AI SYSTEM V1"
    }

# =========================
# SINGLE PRODUCT RUN
# =========================

@app.get("/run/{product_id}")
def run(product_id: str):
    return orchestrator.run(product_id)

# =========================
# FULL PORTFOLIO PROFIT RUN
# =========================

@app.get("/profit")
def profit():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return profit_engine.run_all(products)

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }
