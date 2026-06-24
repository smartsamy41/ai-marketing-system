from fastapi import FastAPI, Request
from datetime import datetime

# =========================
# SAFE CORE APP (NO IMPORT CRASH)
# =========================

app = FastAPI()


# =========================
# SAFE ENGINE WRAPPER
# =========================

class SafeTracking:
    def __init__(self):
        self.clicks = []

    def track_click(self, product_id, source="api"):
        self.clicks.append(product_id)
        return {"status": "CLICK_TRACKED"}

    def get_summary(self):
        return {"clicks": len(self.clicks)}


class SafeTraffic:
    def run_bulk_traffic(self, products):
        return {"status": "OK", "products": products}

    def get_stats(self):
        return {"traffic": 0}


class SafeGovernor:
    def approve(self, product_id, traffic, score):
        return {"status": "APPROVED"}


class SafeLandingpage:
    def get(self, product_id):
        return {"status": "NOT_FOUND"}

    def create(self, product_id, name, category):
        return {
            "status": "CREATED",
            "product_id": product_id,
            "title": name
        }


class SafeAffiliate:
    def get_redirect(self, product_id):
        return {"url": f"/affiliate/{product_id}"}


class SafeConnector:
    def run_cycle(self, product_id, category):
        return {
            "status": "AUTOPILOT_CYCLE_DONE",
            "product_id": product_id
        }


# =========================
# INIT (100% SAFE)
# =========================

tracking = SafeTracking()
traffic = SafeTraffic()
governor = SafeGovernor()
landingpage_engine = SafeLandingpage()
affiliate_router = SafeAffiliate()
connector = SafeConnector()


# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "SAFE MODE"}


@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


@app.get("/engine")
def engine():
    return {"status": "SAFE", "all": True}


@app.get("/run")
def run():
    return connector.run_cycle("CHK24_001", "check24")


@app.get("/autopilot")
def autopilot():
    return connector.run_cycle("CHK24_001", "check24")


@app.get("/loop")
def loop():
    return {
        "traffic": traffic.run_bulk_traffic(["CHK24_001", "TC_001"]),
        "autopilot": connector.run_cycle("CHK24_001", "check24")
    }


@app.get("/traffic")
def get_traffic():
    return traffic.run_bulk_traffic(["CHK24_001", "TC_001"])


@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return tracking.track_click(data.get("product_id"), "api")


@app.get("/dashboard")
def dashboard():
    return {
        "traffic": traffic.get_stats(),
        "tracking": tracking.get_summary(),
        "status": "SAFE_MODE"
    }
