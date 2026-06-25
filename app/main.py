from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "system": "SAFE RESET MODE"}

@app.get("/run")
def run():
    return {
        "status": "SAFE",
        "message": "System reset successful"
    }

@app.get("/health")
def health():
    return {"status": "OK"}
