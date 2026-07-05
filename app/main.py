from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import sys
import os

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
# SAFE ENGINE IMPORTS (IMPORTANT FIX)
# =========================
try:
    from engine.orchestrator_clean_master import OrchestratorCleanMaster
    orchestrator = OrchestratorCleanMaster()
except Exception as e:
    orchestrator = None
    print("Orchestrator load failed:", e)

try:
    from engine.real_publish_layer import RealPublishLayer
    publisher = RealPublishLayer()
except Exception as e:
    publisher = None
    print("Publisher load failed:", e)

# =========================
# MEMORY STORAGE
# =========================
click_log = []
revenue_log = []

# =========================
# AFFILIATE MAP
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# ROOT LANDING PAGE (HTML)
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Free Basics AI System</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                padding: 50px;
            }
            .box {
                background: #1e293b;
                padding: 40px;
                border-radius: 20px;
                width: 70%;
                margin: auto;
                box-shadow: 0 0 20px rgba(0,0,0,0.4);
            }
            a {
                display: inline-block;
                margin-top: 15px;
                padding: 12px 20px;
                background: #22c55e;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🚀 Free Basics AI Marketing System</h1>
            <p>Status: LIVE PRODUCTION</p>

            <a href="/landing?product_id=CHK24_001">⚡ Strom Vergleich</a><br>
            <a href="/landing?product_id=TC_001">☀ Solar Vergleich</a><br>
            <a href="/stats">📊 Stats</a>
        </div>
    </body>
    </html>
    """

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "AI_MARKETING_SYSTEM",
        "time": datetime.utcnow().isoformat()
    }

# =========================
# AUDIT SAFE
# =========================
@app.get("/audit")
def audit():
    try:
        if orchestrator:
            return orchestrator.run_sheet_audit()
        return {"status": "orchestrator_not_ready"}
    except Exception as e:
        return {"error": str(e)}

# =========================
# LANDING PAGE
# =========================
@app.get("/landing")
def landing(product_id: str):
    affiliate = affiliate_map.get(product_id, "#")

    html = f"""
    <html>
    <head>
        <title>{product_id} Vergleich</title>
    </head>
    <body style="font-family:Arial;text-align:center;padding:40px;">

        <h1>{product_id}</h1>

        <p><b>Werbung / Anzeige</b></p>

        <p>Vergleiche Tarife und finde das beste Angebot.</p>

        <a href="{affiliate}" style="padding:12px 20px;background:green;color:white;text-decoration:none;">
            👉 Jetzt vergleichen
        </a>

        <hr>

        <p>Telekom Direktangebot</p>
        <a href="https://free-basics.telekom-profis.de">Shop</a>

        <hr>

        <small>powered by AI Marketing System</small>

    </body>
    </html>
    """

    return HTMLResponse(content=html)

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product_id: str):
    event = {
        "product_id": product_id,
        "time": datetime.utcnow().isoformat()
    }
    click_log.append(event)
    return {"status": "click_saved", "event": event}

# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(amount: float):
    event = {
        "amount": amount,
        "time": datetime.utcnow().isoformat()
    }
    revenue_log.append(event)
    return {"status": "conversion_saved", "event": event}

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
# TRAFFIC INFO
# =========================
@app.get("/traffic")
def traffic():
    return {
        "channels": ["landingpage", "pinterest", "youtube"],
        "status": "ready",
        "seo": True
    }
