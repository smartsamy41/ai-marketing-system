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
# MEMORY STORAGE
# =========================
click_log = []
revenue_log = []

# =========================
# AFFILIATE MAP (BASIC)
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24-link",
    "CHK24_002": "https://example-check24-link",
    "AMZ_001": "https://amazon-partner-link",
    "TC_001": "https://tarifcheck-link"
}

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
# BLOGGER
# =========================
@app.get("/blogger")
def blogger_post():
    if blogger:
        return blogger.publish({"demo": "content"})
    return {"error": "blogger_not_loaded"}

# =========================
# AFFILIATE LINK ENDPOINT
# =========================
@app.get("/affiliate")
def get_affiliate(product_id: str):
    return {
        "product_id": product_id,
        "affiliate_link": affiliate_map.get(product_id, "not_found")
    }

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def track_click(product_id: str, source: str = "direct"):
    event = {
        "product_id": product_id,
        "source": source,
        "affiliate_link": affiliate_map.get(product_id),
        "timestamp": datetime.utcnow().isoformat()
    }
    click_log.append(event)
    return {"status": "click_tracked", "event": event}

# =========================
# CONVERSION TRACKING
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
# STATS DASHBOARD
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

# =========================
# TRAFFIC ENGINE
# =========================
@app.get("/traffic")
def traffic():
    return {
        "seo_ready": True,
        "channels": ["blogger", "pinterest", "youtube"],
        "auto_posting": "enabled"
    }
