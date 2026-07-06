from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# STORAGE
# =========================
clicks = []
conversions = []

# =========================
# AFFILIATE LINKS
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "AMZ_001": "https://amazon.de/dp/XXXX?tag=freebasics-21",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# HOME PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h1>🚀 AI Marketing System</h1>

        <a href="/landing?product_id=CHK24_001">Check24</a><br>
        <a href="/landing?product_id=TC_001">Tarifcheck</a><br>
        <a href="/amazon?product_id=AMZ_001">Amazon</a><br>
        <a href="/stats">Stats</a><br>
    </body>
    </html>
    """

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# LANDING PAGE
# =========================
@app.get("/landing", response_class=HTMLResponse)
def landing(product_id: str):
    link = affiliate_map.get(product_id, "#")

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h1>{product_id}</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="{link}" style="padding:12px 20px;background:green;color:white;">
            Jetzt vergleichen
        </a>

        <hr>
        <a href="https://free-basics.telekom-profis.de">Telekom Direkt</a>
    </body>
    </html>
    """

# =========================
# AMAZON ROUTE
# =========================
@app.get("/amazon")
def amazon(product_id: str):
    return {
        "product_id": product_id,
        "link": affiliate_map.get(product_id, "#")
    }

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product_id: str):
    event = {
        "product_id": product_id,
        "time": datetime.utcnow().isoformat()
    }
    clicks.append(event)
    return {"status": "ok"}

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
    return {"status": "ok"}

# =========================
# STATS
# =========================
@app.get("/stats")
def stats():
    revenue = sum(c["amount"] for c in conversions)

    return {
        "clicks": len(clicks),
        "conversions": len(conversions),
        "revenue": revenue
    }
