from fastapi import FastAPI
from datetime import datetime
import os
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

# =========================
# CORE CLASSES
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
# TARIFCHECK SALES (FIXED)
# =========================

class TarifcheckSales:

    def __init__(self):

        self.username = os.getenv("TARIFCHECK_USERNAME")
        self.password = os.getenv("TARIFCHECK_PASSWORD")
        self.url = os.getenv(
            "TARIFCHECK_API_URL",
            "https://www.tarifcheck-partnerprogramm.de/app/api/leads/"
        )

    def fetch(self):

        # 🔥 DEBUG (WICHTIG)
        print("USERNAME:", self.username)
        print("PASSWORD:", "SET" if self.password else "MISSING")
        print("URL:", self.url)

        if not self.username or not self.password:
            return {
                "type": "sales",
                "status": "SKIPPED",
                "error": "Missing ENV credentials"
            }

        try:
            response = requests.get(
                self.url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=20
            )

            return {
                "type": "sales",
                "status": "OK",
                "code": response.status_code,
                "response": response.text[:200]
            }

        except Exception as e:
            return {
                "type": "sales",
                "status": "ERROR",
                "error": str(e)
            }

sales_engine = TarifcheckSales()

# =========================
# ORCHESTRATOR
# =========================

class Orchestrator:

    def run(self, product_id):

        lp = landingpage.create(product_id)
        track = tracking.track(product_id)

        sales = sales_engine.fetch()

        return {
            "product_id": product_id,
            "landingpage": lp,
            "tracking": track,
            "sales": sales
        }

orchestrator = Orchestrator()

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "LIVE V2"}

@app.get("/env-check")
def env_check():
    return {
        "username": os.getenv("TARIFCHECK_USERNAME"),
        "password": "SET" if os.getenv("TARIFCHECK_PASSWORD") else None,
        "url": os.getenv("TARIFCHECK_API_URL")
    }

@app.get("/run")
def run():

    products = ["CHK24_001", "TC_001", "AMZ_001"]

    return {
        "status": "RUNNING",
        "results": [orchestrator.run(p) for p in products],
        "timestamp": datetime.utcnow().isoformat()
    }
