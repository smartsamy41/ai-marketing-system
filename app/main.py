from fastapi import FastAPI

# =========================
# ENGINE IMPORTS
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
except:
    run_orchestrator = None

from engine.email_system import EmailMarketingEngine, get_all_emails
from engine.data_layer_engine import DataLayer
from engine.revenue_autopilot_engine import RevenueAutopilotEngine
from engine.master_autopilot_engine import MasterAutopilotEngine


# =========================
# INIT SYSTEMS
# =========================
app = FastAPI()

db = DataLayer()

email_engine = EmailMarketingEngine(db.leads)

revenue_engine = RevenueAutopilotEngine(None)

master_engine = MasterAutopilotEngine(
    revenue_engine=revenue_engine,
    email_engine=email_engine,
    tracking_engine=db
)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "24/7 AUTOPILOT READY"
    }


# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "orchestrator": run_orchestrator is not None
    }


# =========================
# RUN ORCHESTRATOR
# =========================
@app.get("/run")
def run():

    if not run_orchestrator:
        return {"status": "ERROR"}

    jobs = [
        {"product_id": "CHK24_001", "category": "check24", "data": {}},
        {"product_id": "TC_001", "category": "tarifcheck", "data": {}},
        {"product_id": "AMZ_001", "category": "amazon", "data": {}}
    ]

    results = []

    for job in jobs:
        try:
            results.append(run_orchestrator(job))
        except Exception as e:
            results.append({"error": str(e)})

    return {
        "status": "RUNNING",
        "results": results
    }


# =========================
# EMAIL CAMPAIGN
# =========================
@app.get("/campaign")
def campaign():
    return email_engine.run_campaign()


# =========================
# TRACKING
# =========================
@app.post("/track")
async def track(request):
    data = await request.json()
    return db.track_event(data.get("type"), data.get("data"))


# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
def dashboard():
    return db.get_dashboard()


# =========================
# MASTER AUTOPILOT (🔥 MAIN CONTROL)
# =========================
@app.get("/autopilot")
def autopilot():

    return master_engine.loop()


# =========================
# EMAILS
# =========================
@app.get("/emails")
def emails():
    return get_all_emails()
