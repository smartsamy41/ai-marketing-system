from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK - ROOT WORKING"}

@app.get("/run")
def run():
    return {"status": "OK - ENDPOINT WORKS"}
