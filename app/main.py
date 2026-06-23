from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK"}

@app.get("/run")
def run():
    return {"status": "RUN OK"}
