from fastapi import FastAPI

from engine.ai_autopilot_engine import AutopilotEngine
from engine.publisher_youtube import YouTubePublisher
from engine.publisher_pinterest import PinterestPublisher
from engine.money_tracking import MoneyTracking
from engine.ai_feedback_loop import AIFeedbackLoop
from engine.content_ai import ContentAI

app = FastAPI(title="FREE BASICS PHASE 7")

# =========================
# INIT SYSTEM
# =========================
content_ai = ContentAI()
tracking = MoneyTracking()
feedback = AIFeedbackLoop(tracking)

youtube = YouTubePublisher()
pinterest = PinterestPublisher()

autopilot = AutopilotEngine(
    ai_core=feedback,
    content_ai=content_ai
)

# =========================
# HOME
# =========================
@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "phase": 7,
        "status": "LIVE AUTOPILOT ACTIVE"
    }

# =========================
# CLICK TRACKING
# =========================
@app.get("/click")
def click(product: str):

    return tracking.log_click(product)

# =========================
# CONVERSION TRACKING
# =========================
@app.get("/conversion")
def conversion(product: str, value: float):

    return tracking.log_conversion(product, value)

# =========================
# AUTOPILOT ENGINE
# =========================
@app.get("/autopilot")
def run_autopilot():

    result = autopilot.run()

    if result["status"] == "WAIT":
        return result

    content = result["content"]

    yt = youtube.publish(content)
    pin = pinterest.publish(content)

    return {
        "autopilot": result,
        "youtube": yt,
        "pinterest": pin
    }

# =========================
# ANALYTICS
# =========================
@app.get("/analytics")
def analytics():

    return feedback.optimize()
