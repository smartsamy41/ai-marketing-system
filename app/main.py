from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

# =========================
# APP INIT
# =========================
app = FastAPI(title="AI_MARKETING_SYSTEM")

# =========================
# MEMORY STORAGE
# =========================
clicks = []
conversions = []

# =========================
# AMAZON ENGINE (INLINE CLEAN)
# =========================
class AmazonAffiliateEngine:
    def __init__(self):
        self.products = {
            "AMZ_001": "https://amazon.de/dp/XXXX?tag=freebasics-21",
            "AMZ_002": "https://amazon.de/dp/YYYY?tag=freebasics-21"
        }

    def get_link(self, product_id: str):
        return self.products.get(product_id, "#")

amazon = AmazonAffiliateEngine()

# =========================
# AFFILIATE MAP (CHECK24 + TARIFCHECK + TELEKOM)
# =========================
affiliate_map = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
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
        <h1>AI Marketing System</h1>

        <a href="/landing?product_id=CHK24_001">Check24</a><br>
        <a href="/landing?product_id=TC_001">Tarifcheck</a><br>
        <a href="/amazon?product_id=AMZ_001">Amazon</a><br>
        <a href="/stats">Stats</a>
    </body>
    </html>
    """

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "AI_MARKETING_SYSTEM"
    }

# =========================
# LANDING PAGE (AFFILIATES)
# =========================
@app.get("/landing", response_class=HTMLResponse)
def landing(product_id: str):
    link = affiliate_map.get(product_id, "#")

    html = f"""
    <html>
    <body style="font-family:Arial;text-align:center;padding:40px;">
        <h1>{product_id}</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="{link}" style="padding:12px 20px;background:green;color:white;text-decoration:none;">
            Jetzt vergleichen
        </a>

        <hr>
        <a href="https://free-basics.telekom-profis.de">Telekom Direkt</a>
    </body>
    </html>
    """

    return HTMLResponse(content=html)

# =========================
# AMAZON ROUTE
# =========================
@app.get("/amazon")
def amazon_route(product_id: str):
    return {
        "product_id": product_id,
        "link": amazon.get_link(product_id)
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
    return {"status": "ok", "event": event}

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
    return {"status": "ok", "event": event}

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

# =========================
# TARIFCHECK (PLACEHOLDER API READY)
# =========================
@app.get("/tarifcheck")
def tarifcheck(product_id: str):
    return {
        "status": "ready",
        "product_id": product_id,
        "note": "API integration next phase"
    }
