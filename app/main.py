from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster
from blogger_publisher_engine import BloggerPublisherEngine
from real_publish_layer import RealPublishLayer

app = FastAPI()

orchestrator = OrchestratorCleanMaster()
blogger = BloggerPublisherEngine()
publisher = RealPublishLayer()

@app.get("/")
def home():
    return {"status": "AI_MARKETING_SYSTEM_RUNNING"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/audit")
def audit():
    return orchestrator.run_sheet_audit()

@app.get("/generate")
def generate():
    return {"status": "generation_ready"}

@app.get("/publish")
def publish():
    return publisher.publish_all()

@app.get("/blogger")
def blogger_post():
    return blogger.publish({"demo": "content"})
