from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK - SERVER STARTED"}

@app.get("/run")
def run():
    return {"status": "OK - RUN WORKS"}
