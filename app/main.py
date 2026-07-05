from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# MEMORY STORAGE
# =========================
click_log = []
revenue_log = []

# =========================
# AFFILIATE LINKS
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# ROOT LANDING PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Free Basics AI Marketing System</title>
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
                box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
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
            <p>Status: LIVE PRODUCTION SYSTEM</p>

            <h3>👉 Angebote starten</h3>

            <a href="/landing?product_id=CHK24_001">⚡ Strom Vergleich</a><br>
            <a href="/landing?product_id=TC_001">☀ Solar Vergleich</a><br>
            <a href="/stats">📊 Stats Dashboard</a>
        </div>

    </body>
    </html>
    """

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok", "system": "AI_MARKETING_RUNNING"}

# =========================
# LANDING PAGE
# =========================
@app.get("/landing")
def landing(product_id: str):
    affiliate = affiliate_map.get(product_id, "#")

    html = f"""
    <html>
    <head>
        <title>{product_id} Angebot</title>
    </head>
    <body style="font-family:Arial;text-align:center;padding:40px;">

        <h1>{product_id}</h1>

        <p><b>Werbung / Anzeige</b></p>

        <p>Vergleiche jetzt die besten Tarife und Angebote.</p>

        <a href="{affiliate}" style="padding:12px 20px;background:green;color:white;text-decoration:none;">
            👉 Jetzt vergleichen
        </a>

        <hr>

        <p>Powered by AI Marketing System</p>

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
# STATS DASHBOARD
# =========================
@app.get("/stats")
def stats():
    return {
        "clicks": len(click_log),
        "conversions": len(revenue_log),
        "revenue": sum([x["amount"] for x in revenue_log]) if revenue_log else 0
    }
