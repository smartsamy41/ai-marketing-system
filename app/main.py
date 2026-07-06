from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="FREE_BASICS")

clicks = []
conversions = []

EMAIL = "samyjendoubi@gmail.com"

links = {
    "CHK24_001": "https://example-check24",
    "TC_001": "https://tarifcheck-link",
    "AMZ_001": "https://amazon.de/dp/XXXX?tag=freebasics-21",
    "TEL_001": "https://free-basics.telekom-profis.de"
}

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Free Basics – Vergleiche & Angebote</title>
        <meta name="description" content="Vergleiche Strom, Kredit, Amazon Produkte und Telekom Angebote">
    </head>

    <body style="font-family:Arial;text-align:center;padding:40px">

        <h1>Free Basics</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="/energie">⚡ Energie</a><br>
        <a href="/finanzen">💰 Finanzen</a><br>
        <a href="/tech">🛒 Tech</a><br>

        <hr>

        <a href="/legal/impressum">Impressum</a> |
        <a href="/legal/datenschutz">Datenschutz</a> |
        <a href="/cookies">Cookies</a>

    </body>
    </html>
    """

# =========================
# ENERGIE
# =========================
@app.get("/energie", response_class=HTMLResponse)
def energie():
    return f"""
    <h1>⚡ Energie Vergleich</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="{links['CHK24_001']}">Strom vergleichen</a><br>
    """

# =========================
# FINANZEN
# =========================
@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():
    return f"""
    <h1>💰 Finanzen Vergleich</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="{links['TC_001']}">Kredit vergleichen</a><br>
    """

# =========================
# TECH (AMAZON + TELEKOM)
# =========================
@app.get("/tech", response_class=HTMLResponse)
def tech():
    return f"""
    <h1>🛒 Tech Angebote</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="{links['AMZ_001']}">Amazon Produkt</a><br>
    <a href="{links['TEL_001']}">Telekom Internet</a><br>
    """

# =========================
# LEGAL
# =========================
@app.get("/legal/impressum", response_class=HTMLResponse)
def impressum():
    return f"""
    <h1>Impressum</h1>
    <p>{EMAIL}</p>
    <p>Free Basics Platform</p>
    """

@app.get("/legal/datenschutz", response_class=HTMLResponse)
def datenschutz():
    return """
    <h1>Datenschutz</h1>
    <p>Cookies & Tracking für Affiliate Systeme</p>
    """

@app.get("/cookies", response_class=HTMLResponse)
def cookies():
    return """
    <h1>Cookie Hinweis</h1>
    <p>Diese Seite nutzt Cookies für Analyse</p>
    <button>Akzeptieren</button>
    <button>Ablehnen</button>
    """

# =========================
# TRACKING
# =========================
@app.get("/click")
def click(product_id: str):
    clicks.append({"id": product_id, "time": datetime.utcnow().isoformat()})
    return {"status": "ok"}

@app.get("/conversion")
def conversion(amount: float):
    conversions.append({"amount": amount})
    return {"status": "ok"}

@app.get("/stats")
def stats():
    return {
        "clicks": len(clicks),
        "conversions": len(conversions),
        "revenue": sum(c["amount"] for c in conversions) if conversions else 0
    }

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}
