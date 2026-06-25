from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "system": "RECOVERY MODE"}

@app.get("/run")
def run():
    return {
        "status": "RECOVERY_RUNNING",
        "message": "System is booting in safe mode"
    }

@app.get("/health")
def health():
    return {"status": "OK"}
