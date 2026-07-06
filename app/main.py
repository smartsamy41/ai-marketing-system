from fastapi import FastAPI

from engine.google_sheets_real import GoogleSheetsReal
from engine.ai_real_optimizer import AIRealOptimizer

app = FastAPI(title="FREE BASICS REAL SYSTEM")

# =========================
# INIT REAL SYSTEM
# =========================
sheets = GoogleSheetsReal("YOUR_SHEET_ID")
ai = AIRealOptimizer(sheets)

# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {
        "system": "FREE BASICS",
        "mode": "PHASE_6_REAL_INTEGRATION",
        "status": "LIVE"
    }

# =========================
# CLICK TRACKING (REAL SHEETS)
# =========================
@app.get("/click")
def click(product: str):

    return sheets.log_click(product)

# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(product: str, value: float):

    return sheets.log_conversion(product, value)

# =========================
# AI PICK BEST PRODUCT
# =========================
@app.get("/ai/best")
def best():

    # (später echte Sheets Read API)
    clicks = [["strom"], ["strom"], ["kredit"]]
    conversions = [[100], [50]]

    return {
        "best_product": ai.pick_best(clicks, conversions)
    }
