from fastapi import FastAPI
import sys
import os
from datetime import datetime

# =========================
# PATH FIX
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "engine"))

# =========================
# SAFE IMPORTS
# =========================
try:
    from engine.orchestrator_clean_master import OrchestratorCleanMaster
except Exception:
    OrchestratorCleanMaster = None

try:
    from blogger_publisher_engine import BloggerPublisherEngine
except Exception:
    BloggerPublisherEngine = None

try:
    from real_publish_layer import RealPublishLayer
except Exception:
    RealPublishLayer = None

# =========================
# APP INIT
# =========================
app = FastAPI(title="AI_MARKETING_SYSTEM")

orchestrator = OrchestratorCleanMaster() if OrchestratorCleanMaster else None
blogger = BloggerPublisherEngine() if BloggerPublisherEngine else None
publisher = RealPublishLayer() if RealPublishLayer else None

# =========================
# MEMORY STORAGE (SIMPLE)
# =========================
click_log = []
revenue_log = []

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
# HEALTH
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

# =========================
# MONETIZATION: CLICK TRACK
# =========================
@app.get("/click")
def track_click(product_id: str, source: str = "direct"):
    event = {
        "product_id": product_id,
        "source": source,
        "timestamp": datetime.utcnow().isoformat()
    }
    click_log.append(event)
    return {"status": "click_tracked", "event": event}

# =========================
# MONETIZATION: CONVERSION TRACK
# =========================
@app.get("/conversion")
def track_conversion(product_id: str, amount: float):
    event = {
        "product_id": product_id,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }
    revenue_log.append(event)
    return {"status": "conversion_tracked", "event": event}

# =========================
# MONETIZATION: STATS
# =========================
@app.get("/stats")
def stats():
    total_clicks = len(click_log)
    total_revenue = sum([x["amount"] for x in revenue_log]) if revenue_log else 0

    return {
        "clicks": total_clicks,
        "conversions": len(revenue_log),
        "revenue": total_revenue
    }
