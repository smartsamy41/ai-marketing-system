from fastapi import FastAPI
import sys
import os

# =========================
# PATH FIX (CRITICAL)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "engine"))

# =========================
# SAFE IMPORTS
# =========================
try:
    from engine.orchestrator_clean_master import OrchestratorCleanMaster
except Exception as e:
    print("Orchestrator import failed:", e)
    OrchestratorCleanMaster = None

try:
    from blogger_publisher_engine import BloggerPublisherEngine
except Exception as e:
    print("Blogger import failed:", e)
    BloggerPublisherEngine = None

try:
    from real_publish_layer import RealPublishLayer
except Exception as e:
    print("Publisher import failed:", e)
    RealPublishLayer = None

# =========================
# APP INIT
# =========================
app = FastAPI(title="AI_MARKETING_SYSTEM")

orchestrator = OrchestratorCleanMaster() if OrchestratorCleanMaster else None
blogger = BloggerPublisherEngine() if BloggerPublisherEngine else None
publisher = RealPublishLayer() if RealPublishLayer else None

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {
        "status": "AI_MARKETING_SYSTEM_RUNNING",
        "orchestrator": orchestrator is not None,
        "blogger": blogger is not None,
        "publisher": publisher is not None
    }

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# AUDIT
# =========================
@app.get("/audit")
def audit():
    if orchestrator:
        return orchestrator.run_sheet_audit()
    return {"error": "orchestrator_not_loaded"}

# =========================
# GENERATE
# =========================
@app.get("/generate")
def generate():
    return {"status": "generation_ready"}

# =========================
# PUBLISH
# =========================
@app.get("/publish")
def publish():
    if publisher:
        return publisher.publish_all()
    return {"error": "publisher_not_loaded"}

# =========================
# BLOGGER TEST
# =========================
@app.get("/blogger")
def blogger_post():
    if blogger:
        return blogger.publish({"demo": "content"})
    return {"error": "blogger_not_loaded"}
