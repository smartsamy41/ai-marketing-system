from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="FREE BASICS")

# =========================
# TRACKING STORAGE
# =========================
clicks = []
conversions = []

EMAIL = "samyjendoubi@gmail.com"


# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
        <title>Free Basics – Vergleiche & Angebote</title>
        <meta name="description" content="Vergleiche Energie, Finanzen, Amazon und Telekom Angebote">
        <meta name="robots" content="index, follow">
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>Free Basics</h1>

        <p><b>Werbung / Anzeige</b></p>

        <a href="/energie">⚡ Energie (Check24)</a><br>
        <a href="/finanzen">💰 Finanzen (Tarifcheck)</a><br>
        <a href="/tech">🛒 Tech (Amazon)</a><br>
        <a href="/telekom">📡 Telekom</a><br>

        <hr>

        <a href="/legal/impressum">Impressum</a> |
        <a href="/legal/datenschutz">Datenschutz</a>

    </body>
    </html>
    """


# =========================
# ENERGIE (CHECK24 ONLY)
# =========================
@app.get("/energie", response_class=HTMLResponse)
def energie():

    return """
    <html>
    <head>
        <title>Energie Vergleich – Strom & Gas</title>
        <meta name="description" content="Vergleiche Strom und Gas Tarife">
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>⚡ Energie</h1>
        <p><b>Werbung / Anzeige</b></p>

        <a href="/click?product=strom">Strom vergleichen</a><br>
        <a href="/click?product=gas">Gas vergleichen</a><br>

        <br>
        <a href="/">← Zurück</a>

    </body>
    </html>
    """


# =========================
# FINANZEN (TARIFCHECK ONLY)
# =========================
@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():

    return """
    <html>
    <head>
        <title>Finanzen Vergleich – Kredit & Konto</title>
        <meta name="description" content="Vergleiche Kredite und Konten">
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>💰 Finanzen</h1>
        <p><b>Werbung / Anzeige</b></p>

        <a href="/click?product=kredit">Kredit vergleichen</a><br>
        <a href="/click?product=girokonto">Girokonto vergleichen</a><br>

        <br>
        <a href="/">← Zurück</a>

    </body>
    </html>
    """


# =========================
# TECH (AMAZON ONLY)
# =========================
@app.get("/tech", response_class=HTMLResponse)
def tech():

    return """
    <html>
    <head>
        <title>Amazon Tech Produkte</title>
        <meta name="description" content="Amazon Produkte vergleichen">
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>🛒 Tech</h1>
        <p><b>Werbung / Anzeige</b></p>

        <a href="/click?product=laptop">Laptop</a><br>
        <a href="/click?product=headphones">Headphones</a><br>

        <br>
        <a href="/">← Zurück</a>

    </body>
    </html>
    """


# =========================
# TELEKOM ONLY
# =========================
@app.get("/telekom", response_class=HTMLResponse)
def telekom():

    return """
    <html>
    <head>
        <title>Telekom Angebote</title>
        <meta name="description" content="Telekom Internet & Mobilfunk">
    </head>

    <body style="font-family:Arial;text-align:center;padding:30px">

        <h1>📡 Telekom</h1>
        <p><b>Werbung / Anzeige</b></p>

        <a href="https://free-basics.telekom-profis.de">Magenta Tarife</a><br>

        <br>
        <a href="/">← Zurück</a>

    </body>
    </html>
    """


# =========================
# TRACKING CLICK
# =========================
@app.get("/click")
def click(product: str, source: str = "direct"):

    clicks.append({
        "product": product,
        "source": source,
        "time": datetime.utcnow().isoformat()
    })

    return {
        "status": "tracked",
        "product": product
    }


# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(product: str, value: float):

    conversions.append({
        "product": product,
        "value": value,
        "time": datetime.utcnow().isoformat()
    })

    return {
        "status": "conversion_saved",
        "product": product,
        "value": value
    }


# =========================
# STATS DASHBOARD
# =========================
@app.get("/stats")
def stats():

    revenue = sum(c["value"] for c in conversions) if conversions else 0

    return {
        "clicks": len(clicks),
        "conversions": len(conversions),
        "revenue": revenue
    }


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
    <p>DSGVO konform Tracking aktiv</p>
    """
