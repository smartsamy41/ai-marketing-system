from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from engine.sheets_connector import SheetsConnector
from engine.ai_autopilot_engine import AIAutopilotEngine
from engine.content_generator import ContentGenerator
from engine.publish_engine import PublishEngine

app = FastAPI(title="FREE BASICS")

# =========================
# INIT SYSTEM
# =========================
sheets = SheetsConnector()
ai = AIAutopilotEngine(sheets)
content = ContentGenerator()
publisher = PublishEngine()

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
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product: str):

    sheets.write_click(product)

    return {"status": "tracked", "product": product}

# =========================
# AI AUTOPILOT RUN
# =========================
@app.get("/autopilot")
def autopilot():

    decision = ai.decide()

    if decision["action"] == "WAIT":
        return decision

    product = decision["product"]

    content_data = content.generate(product)

    yt = publisher.publish_youtube(content_data)
    pin = publisher.publish_pinterest(content_data)

    return {
        "decision": decision,
        "content": content_data,
        "youtube": yt,
        "pinterest": pin
    }

# =========================
# SIMPLE LANDING PAGES
# =========================
@app.get("/energie", response_class=HTMLResponse)
def energie():
    return "<h1>Energie</h1><a href='/click?product=strom'>Strom</a>"

@app.get("/finanzen", response_class=HTMLResponse)
def finanzen():
    return "<h1>Finanzen</h1><a href='/click?product=kredit'>Kredit</a>"

@app.get("/tech", response_class=HTMLResponse)
def tech():
    return "<h1>Tech</h1><a href='/click?product=laptop'>Laptop</a>"

@app.get("/telekom", response_class=HTMLResponse)
def telekom():
    return "<h1>Telekom</h1><a href='https://free-basics.telekom-profis.de'>Magenta</a>"
