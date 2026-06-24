from fastapi import FastAPI, Request

# =========================
# SAFE IMPORTS
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
except Exception:
    run_orchestrator = None

from engine.data_layer_engine import DataLayer


# =========================
# APP INIT
# =========================
app = FastAPI()

db = DataLayer()


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "LIVE"
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
        return {
            "status": "ERROR",
            "message": "orchestrator not loaded"
        }

    jobs = [
        {"product_id": "CHK24_001", "category": "check24", "data": {}},
        {"product_id": "TC_001", "category": "tarifcheck", "data": {}},
        {"product_id": "AMZ_001", "category": "amazon", "data": {}}
    ]

    results = []

    for job in jobs:

        try:
            result = run_orchestrator(job)

            results.append({
                "product_id": job["product_id"],
                "status": "SUCCESS",
                "result": result
            })

        except Exception as e:

            results.append({
                "product_id": job["product_id"],
                "status": "ERROR",
                "message": str(e)
            })

    return {
        "status": "RUNNING_ORCHESTRATOR",
        "total_jobs": len(results),
        "results": results
    }


# =========================
# EMAIL / LEAD TRACKING
# =========================
@app.post("/track")
async def track(request: Request):

    data = await request.json()

    return db.track_event(
        data.get("type", "unknown"),
        data.get("data", {})
    )


# =========================
# DASHBOARD (MONEY VIEW)
# =========================
@app.get("/dashboard")
def dashboard():

    return {
        "status": "OK",
        "data": db.get_dashboard()
    }


# =========================
# EMAIL VIEW
# =========================
@app.get("/leads")
def leads():

    return {
        "status": "OK",
        "leads": db.leads
    }


# =========================
# SALES VIEW
# =========================
@app.get("/sales")
def sales():

    return {
        "status": "OK",
        "sales": db.sales
    }


# =========================
# EVENTS VIEW
# =========================
@app.get("/events")
def events():

    return {
        "status": "OK",
        "events": db.events
    }


# =========================
# ENGINE STATUS
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "ENGINE OK",
        "orchestrator": run_orchestrator is not None,
        "data_layer": True
    }
