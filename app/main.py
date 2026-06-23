from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK", "message": "container started"}

@app.get("/run")
def run():
    return {"status": "OK", "message": "run endpoint working"}
