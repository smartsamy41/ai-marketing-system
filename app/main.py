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
except:
    OrchestratorCleanMaster = None

try:
    from blogger_publisher_engine import BloggerPublisherEngine
except:
    BloggerPublisherEngine = None

try:
    from real_publish_layer import RealPublishLayer
except:
    RealPublishLayer = None

# =========================
# APP INIT
# =========================
app = FastAPI(title="AI_MARKETING_SYSTEM")

orchestrator = OrchestratorCleanMaster() if OrchestratorCleanMaster else None
blogger = BloggerPublisherEngine() if BloggerPublisherEngine else None
publisher = RealPublishLayer() if RealPublishLayer else None

# =========================
# MEMORY
# =========================
click_log = []
revenue_log = []
performance_log = {}

# Affiliate Map
affiliate_map = {
    "CHK24_001": "https://example-check24-link",
    "AMZ_001": "https://amazon-link",
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
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product_id: str, source: str = "direct"):
    event = {
        "product_id": product_id,
        "source": source,
        "affiliate": affiliate_map.get(product_id),
        "timestamp": datetime.utcnow().isoformat()
    }
    click_log.append(event)
    return {"status": "click_tracked", "event": event}

# =========================
# CONVERSION
# =========================
@app.get("/conversion")
def conversion(product_id: str, amount: float):
    event = {
        "product_id": product_id,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }
    revenue_log.append(event)
    return {"status": "conversion_tracked", "event": event}

# =========================
# STATS
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
# LANDINGPAGE GENERATOR
# =========================
@app.get("/landingpage")
def landingpage(product_id: str):
    affiliate = affiliate_map.get(product_id, "#")

    html = f"""
    <html>
    <head><title>{product_id}</title></head>
    <body>
        <h1>{product_id} Angebot</h1>
        <p>Beste Deals automatisch generiert</p>
        <a href="{affiliate}">Jetzt vergleichen</a>
    </body>
    </html>
    """

    return {
        "product_id": product_id,
        "html": html,
        "affiliate": affiliate
    }

# =========================
# LEARNING ENGINE
# =========================
@app.get("/learn")
def learn(product_id: str, clicks: int, conversions: int):
    score = conversions / clicks if clicks > 0 else 0

    performance_log[product_id] = {
        "clicks": clicks,
        "conversions": conversions,
        "score": score
    }

    return {
        "product_id": product_id,
        "score": score
    }
