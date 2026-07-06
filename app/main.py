from fastapi import FastAPI

from engine.sheets_api import SheetsAPI
from engine.ai_core_engine import AICoreEngine
from engine.content_ai import ContentAI
from engine.autopilot_engine import AutopilotEngine

app = FastAPI(title="FREE BASICS AI AUTOPILOT")

# =========================
# SYSTEM INIT
# =========================
sheets = SheetsAPI()
ai = AICoreEngine(sheets)
content = ContentAI()
autopilot = AutopilotEngine(ai, content)

# =========================
# HOME
# =========================
@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "status": "LIVE",
        "mode": "PHASE_5_AUTOPILOT"
    }

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product: str):

    sheets.write_click(product)

    return {"status": "tracked", "product": product}

# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(product: str, value: float):

    sheets.write_conversion(product, value)

    return {"status": "conversion_saved"}

# =========================
# AI AUTOPILOT RUN
# =========================
@app.get("/autopilot")
def run_autopilot():

    result = autopilot.run()

    return result

# =========================
# DEBUG DATA
# =========================
@app.get("/data")
def data():

    return sheets.export()
