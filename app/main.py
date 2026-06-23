from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK"}

@app.get("/run")
def run():
    return {"status": "RUN OK"}

@app.get("/health")
def health():
    return {"status": "HEALTH OK"}
