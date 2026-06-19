from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

print("🟢 AI SYSTEM STARTED")


@app.get("/")
def root():
    return {
        "status": "AI SYSTEM ONLINE",
        "time": str(datetime.now())
    }


@app.get("/health")
def health():
    return {
        "status": "RUNNING",
        "system": "CLEAN_APP_MAIN",
        "time": str(datetime.now())
    }


@app.get("/run")
def run_system():
    try:
        from engine.master_engine import run_master_engine

        result = run_master_engine()

        return {
            "status": result.get("status", "UNKNOWN"),
            "mode": result.get("mode", "MASTER_ENGINE"),
            "executed": result.get("executed", 0),
            "results": result.get("results", []),
            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "FATAL_ERROR",
            "message": str(e),
            "time": str(datetime.now())
        }
