from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "system": "SAFE MODE STABLE"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/run")
def run():
    return {
        "status": "SAFE",
        "message": "System stabilized - waiting for modules"
    }
