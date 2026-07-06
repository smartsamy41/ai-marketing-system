from fastapi import FastAPI

from engine.cloud_scheduler_trigger import CloudSchedulerTrigger
from engine.secret_manager import SecretManager

app = FastAPI(title="FREE BASICS PHASE 10")

# =========================
# INIT SYSTEM
# =========================
secrets = SecretManager()

# orchestrator kommt aus Phase 9 (extern injected)
orchestrator = None

trigger = CloudSchedulerTrigger(orchestrator)

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "phase": 10,
        "status": "GLOBAL PRODUCTION READY"
    }

# =========================
# CLOUD RUN TRIGGER ENTRY
# =========================
@app.post("/run")
def run_system():

    return trigger.execute()
