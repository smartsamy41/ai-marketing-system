from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from engine.sheets_engine import SheetsEngine
from engine.ai_learning_engine import AILearningEngine

app = FastAPI(title="FREE BASICS")

# =========================
# SYSTEM INIT
# =========================
sheets = SheetsEngine()
ai = AILearningEngine(sheets)

# =========================
# HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <h1>Free Basics</h1>
    <p>Werbung / Anzeige</p>

    <a href="/energie">Energie</a><br>
    <a href="/finanzen">Finanzen</a><br>
    <a href="/tech">Tech</a><br>
    <a href="/telekom">Telekom</a><br>
    """

# =========================
# CLICK TRACKING ROUTE
# =========================
@app.get("/click")
def click(product: str):

    result = sheets.log_click(product)

    return {
        "status": "ok",
        "data": result
    }

# =========================
# CONVERSION TRACKING ROUTE
# =========================
@app.get("/conversion")
def conversion(product: str, value: float):

    result = sheets.log_conversion(product, value)

    return {
        "status": "ok",
        "data": result
    }

# =========================
# AI ANALYSIS
# =========================
@app.get("/ai")
def ai_analysis():

    return ai.analyze()

# =========================
# HOME PAGES
# =========================
@app.get("/energie", response_class=HTMLResponse)
def energie():
    return """
    <h1>Energie</h1>
    <p>Werbung / Anzeige</p>
    <a href="/click?product=strom">Strom</a><br>
    <a href="/click?product=gas">Gas</a><br>
    """

@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():
    return """
    <h1>Finanzen</h1>
    <p>Werbung / Anzeige</p>
    <a href="/click?product=kredit">Kredit</a><br>
    <a href="/click?product=girokonto">Girokonto</a><br>
    """

@app.get("/tech", response_class=HTMLResponse)
def tech():
    return """
    <h1>Tech</h1>
    <p>Werbung / Anzeige</p>
    <a href="/click?product=laptop">Laptop</a><br>
    <a href="/click?product=headphones">Headphones</a><br>
    """

@app.get("/telekom", response_class=HTMLResponse)
def telekom():
    return """
    <h1>Telekom</h1>
    <p>Werbung / Anzeige</p>
    <a href="https://free-basics.telekom-profis.de">Magenta</a><br>
    """
