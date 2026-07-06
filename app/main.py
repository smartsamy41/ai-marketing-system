from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="FREE_BASICS")

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
    </head>

    <body style="font-family:Arial;text-align:center;padding:40px">

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
    <h1>⚡ Energie</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="#">Strom Vergleich</a><br>
    <a href="#">Gas Vergleich</a><br>
    <a href="#">DSL</a><br>
    """

# =========================
# FINANZEN (TARIFCHECK ONLY)
# =========================
@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():
    return """
    <h1>💰 Finanzen</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="#">Kredit</a><br>
    <a href="#">Girokonto</a><br>
    <a href="#">Versicherung</a><br>
    """

# =========================
# TECH (AMAZON ONLY)
# =========================
@app.get("/tech", response_class=HTMLResponse)
def tech():
    return """
    <h1>🛒 Amazon Produkte</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="#">Produkt 1</a><br>
    <a href="#">Produkt 2</a><br>
    """

# =========================
# TELEKOM (ONLY)
# =========================
@app.get("/telekom", response_class=HTMLResponse)
def telekom():
    return """
    <h1>📡 Telekom</h1>
    <p><b>Werbung / Anzeige</b></p>

    <a href="https://free-basics.telekom-profis.de">Magenta Tarife</a><br>
    """

# =========================
# LEGAL
# =========================
@app.get("/legal/impressum", response_class=HTMLResponse)
def impressum():
    return f"<h1>Impressum</h1><p>{EMAIL}</p>"

@app.get("/legal/datenschutz", response_class=HTMLResponse)
def datenschutz():
    return "<h1>Datenschutz</h1><p>Tracking aktiv</p>"
