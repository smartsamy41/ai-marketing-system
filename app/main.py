from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI_MARKETING_SYSTEM_RUNNING"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/generate")
def generate():
    return {"status": "generation_endpoint_ready"}

@app.get("/publish")
def publish():
    return {"status": "publish_endpoint_ready"}
