from fastapi import FastAPI

app = FastAPI()

# =========================
# MINIMAL SAFE SYSTEM
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "MINIMAL MODE ACTIVE"
    }

@app.get("/run")
def run():
    return {
        "status": "RUNNING",
        "mode": "SAFE",
        "message": "System is stable - no orchestration loaded"
    }

@app.get("/health")
def health():
    return {
        "status": "OK"
    }
