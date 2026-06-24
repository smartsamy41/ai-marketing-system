from fastapi import FastAPI, Request

# =========================
# ENGINE IMPORTS SAFE
# =========================
try:
    from engine.orchestrator_engine_v2 import run_orchestrator
except Exception:
    run_orchestrator = None

from engine.email_system import (
    add_email,
    confirm_email,
    get_active_emails,
    get_all_emails
)


app = FastAPI()


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
# EMAIL SIGNUP (LANDINGPAGE)
# =========================
@app.post("/subscribe")
async def subscribe(request: Request):

    data = await request.json()
    email = data.get("email", "")

    return add_email(email)


# =========================
# EMAIL CONFIRM (DOI)
# =========================
@app.get("/confirm/{email_id}")
def confirm(email_id: str):

    return confirm_email(email_id)


# =========================
# EMAIL LISTS
# =========================
@app.get("/emails")
def emails():

    return get_active_emails()


@app.get("/emails/all")
def emails_all():

    return get_all_emails()


# =========================
# ENGINE STATUS
# =========================
@app.get("/engine")
def engine():

    return {
        "status": "ENGINE OK",
        "orchestrator": run_orchestrator is not None,
        "email_system": True
    }
