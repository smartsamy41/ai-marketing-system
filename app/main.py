from fastapi import FastAPI
from engine.scheduler_loop import SchedulerLoop

app = FastAPI(title="FREE BASICS PHASE 9")

# =========================
# SYSTEM STATUS
# =========================
@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "phase": 9,
        "status": "FULL AUTONOMOUS AI LOOP READY"
    }

# =========================
# START AUTONOMOUS LOOP
# =========================
@app.get("/start")
def start_loop(orchestrator):

    scheduler = SchedulerLoop(orchestrator)

    scheduler.start(interval_seconds=300)

    return {
        "status": "loop_started"
    }
