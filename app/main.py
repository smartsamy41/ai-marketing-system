from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================
# SAFE ENGINE (MINIMAL STABLE)
# =========================

class TrackingEngine:
    def __init__(self):
        self.clicks = []

    def track_click(self, product_id, source="api"):
        self.clicks.append(product_id)
        return {"status": "CLICK_TRACKED"}

    def get_summary(self):
        return {"clicks": len(self.clicks)}


class TrafficEngine:
    def run_bulk_traffic(self, products):
        return {"status": "OK", "products": products}

    def get_stats(self):
        return {"traffic": 0}


class Governor:
    def approve(self, product_id, traffic, score):
        return {"status": "APPROVED"}


class SalesEngine:
    def send_lead(self, product_id, source="api"):
        return {"status": "LEAD_SENT", "product_id": product_id}

    def get_sales_stats(self):
        return {"sales": 0}


class Connector:
    def run_cycle(self, product_id, category):
        return {
            "status": "AUTOPILOT_CYCLE_DONE",
            "product_id": product_id
        }


# =========================
# INIT
# =========================

tracking = TrackingEngine()
traffic = TrafficEngine()
governor = Governor()
sales = SalesEngine()
connector = Connector()


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "OK", "system": "STABLE MODE"}


@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


@app.get("/engine")
def engine():
    return {
        "tracking": True,
        "traffic": True,
        "sales": True,
        "governor": True
    }


# =========================
# FLOW (MAIN)
# =========================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    decision = governor.approve(product_id, 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    tracking.track_click(product_id, "flow")
    sales.send_lead(product_id, "flow")

    result = connector.run_cycle(product_id, "check24")

    return {
        "status": "FLOW_COMPLETE",
        "timestamp": datetime.utcnow().isoformat(),
        "autopilot": result,
        "sales": sales.send_lead(product_id, "flow")
    }


# =========================
# RUN
# =========================

@app.get("/run")
def run():
    return connector.run_cycle("CHK24_001", "check24")


# =========================
# AUTOPILOT
# =========================

@app.get("/autopilot")
def autopilot():
    return connector.run_cycle("CHK24_001", "check24")


# =========================
# LOOP
# =========================

@app.get("/loop")
def loop():
    return {
        "traffic": traffic.run_bulk_traffic(["CHK24_001", "TC_001"]),
        "autopilot": connector.run_cycle("CHK24_001", "check24")
    }


# =========================
# TRAFFIC
# =========================

@app.get("/traffic")
def get_traffic():
    return traffic.run_bulk_traffic(["CHK24_001", "TC_001"])


# =========================
# TRACK
# =========================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return tracking.track_click(data.get("product_id"))


# =========================
# SALES
# =========================

@app.get("/sales")
def sales_status():
    return sales.get_sales_stats()


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():
    return {
        "traffic": traffic.get_stats(),
        "tracking": tracking.get_summary(),
        "sales": sales.get_sales_stats(),
        "status": "STABLE"
    }
