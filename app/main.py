from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK - RUNNING"}

@app.get("/run")
def run():
    return {"status": "OK - ENDPOINT WORKS"}
