from fastapi import FastAPI

app = FastAPI(title="FREE BASICS PHASE 8")

@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "phase": 8,
        "status": "REAL MONEY AUTOPILOT ACTIVE"
    }
