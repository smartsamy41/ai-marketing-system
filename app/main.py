from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse

from engine.affiliate_engine import get_affiliate_link
from engine.tracking_engine import track_click, track_conversion, get_stats

app = FastAPI(title="FREE BASICS")

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Free Basics</h1>
    <p>Werbung / Anzeige</p>

    <a href='/energie'>Energie</a><br>
    <a href='/finanzen'>Finanzen</a><br>
    <a href='/tech'>Tech</a><br>
    <a href='/telekom'>Telekom</a><br>
    """


# =========================
# CLICK ROUTER (MONEY CORE)
# =========================
@app.get("/click")
def click(product: str):

    track_click(product)

    url = get_affiliate_link(product)

    return RedirectResponse(url)


# =========================
# ENERGIE
# =========================
@app.get("/energie", response_class=HTMLResponse)
def energie():
    return """
    <h1>Energie</h1>
    <p>Werbung / Anzeige</p>

    <a href="/click?product=strom">Strom vergleichen</a><br>
    <a href="/click?product=gas">Gas vergleichen</a><br>
    """


# =========================
# FINANZEN
# =========================
@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():
    return """
    <h1>Finanzen</h1>
    <p>Werbung / Anzeige</p>

    <a href="/click?product=kredit">Kredit</a><br>
    <a href="/click?product=girokonto">Girokonto</a><br>
    """


# =========================
# TECH
# =========================
@app.get("/tech", response_class=HTMLResponse)
def tech():
    return """
    <h1>Tech</h1>
    <p>Werbung / Anzeige</p>

    <a href="/click?product=laptop">Laptop</a><br>
    <a href="/click?product=headphones">Headphones</a><br>
    """


# =========================
# TELEKOM
# =========================
@app.get("/telekom", response_class=HTMLResponse)
def telekom():
    return """
    <h1>Telekom</h1>
    <p>Werbung / Anzeige</p>

    <a href="/click?product=telekom">Magenta Tarife</a><br>
    """


# =========================
# STATS (LIVE SYSTEM)
# =========================
@app.get("/stats")
def stats():
    return get_stats()
