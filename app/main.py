from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# SAFE STATE STORAGE
# =========================
clicks = []
conversions = []

# =========================
# AFFILIATE MAP (SIMPLE CORE)
# =========================
AFFILIATE = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# ROOT WEBSITE (HTML)
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
            .card {
                background: #1e293b;
                padding: 40px;
                border-radius: 20px;
                width: 70%;
                margin: auto;
            }
            a {
                display: inline-block;
                margin: 10px;
                padding: 12px 18px;
                background: #22c55e;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 AI Marketing System</h1>
            <p>Status: LIVE</p>

            <a href="/landing?product_id=CHK24_001">⚡ Strom Vergleich</a>
            <a href="/landing?product_id=TC_001">☀ Solar Vergleich</a>
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
# LANDING PAGE (DYNAMIC)
# =========================
@app.get("/landing", response_class=HTMLResponse)
def landing(product_id: str):
    link = AFFILIATE.get(product_id, "#")

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h1>{product_id}</h1>

        <p><b>Werbung / Anzeige</b></p>

        <p>Vergleiche Tarife und finde das beste Angebot.</p>

        <a href="{link}" style="padding:12px 20px;background:green;color:white;text-decoration:none;">
            👉 Jetzt vergleichen
        </a>

        <hr>

        <p>Telekom Direktlink</p>
        <a href="https://free-basics.telekom-profis.de">Shop</a>

    </body>
    </html>
    """

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product_id: str):
    event = {
        "product": product_id,
        "time": datetime.utcnow().isoformat()
    }
    clicks.append(event)
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
    conversions.append(event)
    return {"status": "conversion_saved", "event": event}

# =========================
# STATS
# =========================
@app.get("/stats")
def stats():
    return {
        "clicks": len(clicks),
        "conversions": len(conversions),
        "revenue": sum([c["amount"] for c in conversions]) if conversions else 0
    }

# =========================
# TRAFFIC INFO
# =========================
@app.get("/traffic")
def traffic():
    return {
        "channels": ["landingpage", "seo", "social"],
        "status": "active"
    }
