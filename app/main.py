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
# APP INIT
# =========================
app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# SAFE IMPORTS
# =========================
try:
    from engine.orchestrator_clean_master import OrchestratorCleanMaster
    orchestrator = OrchestratorCleanMaster()
except:
    orchestrator = None

try:
    from real_publish_layer import RealPublishLayer
    publisher = RealPublishLayer()
except:
    publisher = None

# =========================
# MEMORY SYSTEM
# =========================
click_log = []
revenue_log = []

# =========================
# AFFILIATE LINKS (PLACEHOLDER)
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {
        "status": "AI_MARKETING_SYSTEM_RUNNING",
        "orchestrator": orchestrator is not None,
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
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product_id: str, source: str = "landingpage"):
    event = {
        "product_id": product_id,
        "source": source,
        "time": datetime.utcnow().isoformat(),
        "affiliate": affiliate_map.get(product_id)
    }
    click_log.append(event)
    return {"status": "click_tracked", "event": event}

# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(product_id: str, amount: float):
    event = {
        "product_id": product_id,
        "amount": amount,
        "time": datetime.utcnow().isoformat()
    }
    revenue_log.append(event)
    return {"status": "conversion_tracked", "event": event}

# =========================
# STATS
# =========================
@app.get("/stats")
def stats():
    return {
        "clicks": len(click_log),
        "conversions": len(revenue_log),
        "revenue": sum([x["amount"] for x in revenue_log]) if revenue_log else 0
    }

# =========================
# LANDINGPAGE API
# =========================
@app.get("/landing")
def landing(product_id: str):
    affiliate = affiliate_map.get(product_id, "#")

    html = f"""
    <html>
    <head>
        <title>{product_id} Vergleich</title>
    </head>
    <body>

        <h1>{product_id} Angebot</h1>

        <p><b>Werbung / Anzeige</b></p>

        <p>Vergleiche Tarife und finde das beste Angebot.</p>

        <a href="{affiliate}">
            👉 Jetzt vergleichen
        </a>

        <hr>

        <p>Telekom Direktangebot:</p>
        <a href="https://free-basics.telekom-profis.de">
            Telekom Shop
        </a>

        <hr>

        <small>
            powered by TARIFCHECK24 GmbH
        </small>

    </body>
    </html>
    """

    return {
        "product_id": product_id,
        "html": html,
        "affiliate": affiliate
    }

# =========================
# TRAFFIC INFO
# =========================
@app.get("/traffic")
def traffic():
    return {
        "channels": ["landingpage", "pinterest", "youtube"],
        "status": "ready",
        "seo": True
    }
