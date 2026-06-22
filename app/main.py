from fastapi import FastAPI
from datetime import datetime

from engine.master_engine import run_master_engine

app = FastAPI()

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
        "system": "CLEAN_PRODUCTION",
        "time": str(datetime.now())
    }

@app.get("/run")
def run():
    try:
        result = run_master_engine()
        return result
    except Exception as e:
        return {
            "status": "FATAL_ERROR",
            "error": str(e),
            "time": str(datetime.now())
        }
