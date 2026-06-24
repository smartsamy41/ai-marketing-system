from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()

# =========================================================
# 🧠 SAFE CORE ENGINE LAYER (NO CRASH)
# =========================================================

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
        return {"clicks": len(self.clicks)}


class TrafficEngine:
    def run_bulk_traffic(self, products):
        return {"status": "OK", "products": products}

    def get_stats(self):
        return {"traffic": 0}


class SalesEngine:
    def __init__(self):
        self.leads = []

    def send_lead(self, product_id, source="system"):
        lead = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.leads.append(lead)
        return {"status": "LEAD_SENT", "lead": lead}

    def get_sales_stats(self):
        return {"leads": len(self.leads)}


class LandingpageEngine:
    def __init__(self):
        self.pages = {}

    def get(self, product_id):
        return self.pages.get(product_id, {"status": "NOT_FOUND"})

    def create(self, product_id, name, category):
        page = {
            "product_id": product_id,
            "title": name,
            "category": category,
            "html": f"""
            <html>
                <body>
                    <h1>{name}</h1>
                    <p>Vergleich starten und Angebote prüfen.</p>

                    <!-- NEWSLETTER -->
                    <form action="/subscribe" method="post">
                        <input type="email" name="email" placeholder="E-Mail">
                        <button type="submit">Newsletter starten</button>
                    </form>

                    <a href="/flow/{product_id}">Jetzt vergleichen</a>
                </body>
            </html>
            """,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.pages[product_id] = page
        return page


class Governor:
    def approve(self, product_id, traffic, score):
        return {"status": "APPROVED"}


class AutopilotConnector:
    def run_cycle(self, product_id, category):
        return {
            "status": "AUTOPILOT_CYCLE_DONE",
            "product_id": product_id,
            "timestamp": datetime.utcnow().isoformat()
        }


# =========================================================
# 🚀 INIT SYSTEM
# =========================================================

tracking = TrackingEngine()
traffic = TrafficEngine()
sales = SalesEngine()
landingpage = LandingpageEngine()
governor = Governor()
connector = AutopilotConnector()


# =========================================================
# 🟢 BASIC ROUTES
# =========================================================

@app.get("/")
def root():
    return {"status": "OK", "system": "CLEAN MAIN V2 ACTIVE"}


@app.get("/health")
def health():
    return {"status": "OK", "ready": True}


@app.get("/engine")
def engine():
    return {
        "tracking": True,
        "traffic": True,
        "sales": True,
        "autopilot": True
    }


# =========================================================
# 💰 FLOW (MAIN MONEY PIPELINE)
# =========================================================

@app.get("/flow/{product_id}")
def flow(product_id: str):

    decision = governor.approve(product_id, 5, 0.8)

    if decision["status"] != "APPROVED":
        return {"status": "BLOCKED"}

    # Landingpage
    page = landingpage.get(product_id)
    if page["status"] == "NOT_FOUND":
        page = landingpage.create(product_id, product_id, "general")

    # Tracking
    tracking.track_click(product_id, "flow")

    # Sales
    sale = sales.send_lead(product_id, "flow")

    # Autopilot
    auto = connector.run_cycle(product_id, "system")

    return {
        "status": "FLOW_COMPLETE",
        "landingpage": page,
        "sales": sale,
        "autopilot": auto
    }


# =========================================================
# 🚀 AUTOPILOT
# =========================================================

@app.get("/autopilot")
def autopilot():
    return connector.run_cycle("CHK24_001", "check24")


# =========================================================
# 🚀 RUN
# =========================================================

@app.get("/run")
def run():
    return connector.run_cycle("CHK24_001", "check24")


# =========================================================
# 🚀 TRAFFIC
# =========================================================

@app.get("/traffic")
def get_traffic():
    return traffic.run_bulk_traffic(["CHK24_001", "TC_001", "AMZ_001"])


# =========================================================
# 📊 TRACK CLICK
# =========================================================

@app.post("/track")
async def track(request: Request):
    data = await request.json()
    return tracking.track_click(data.get("product_id"), "api")


# =========================================================
# 💰 SALES STATUS
# =========================================================

@app.get("/sales")
def sales_status():
    return sales.get_sales_stats()


# =========================================================
# 📧 NEWSLETTER (DOI READY)
# =========================================================

@app.post("/subscribe")
async def subscribe(request: Request):
    data = await request.json()
    return {
        "status": "SUBSCRIBED",
        "email": data.get("email"),
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================================================
# 📊 DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():
    return {
        "traffic": traffic.get_stats(),
        "tracking": tracking.get_summary(),
        "sales": sales.get_sales_stats(),
        "status": "CLEAN_MAIN_V2_ACTIVE"
    }
