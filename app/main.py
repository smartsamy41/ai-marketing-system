from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "mode": "MINIMAL"}

@app.get("/run")
def run():
    return {"status": "RUNNING", "message": "minimal system active"}
