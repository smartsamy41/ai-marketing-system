from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from engine.cloud_scheduler_trigger import CloudSchedulerTrigger

from engine.sheets_engine import SheetsEngine
from engine.ai_core_engine import AICoreEngine
from engine.content_ai import ContentAI

from engine.revenue_engine import RevenueEngine
from engine.ai_learning_engine import AILearningLoop

from engine.autopilot_orchestrator import AutopilotOrchestrator
from engine.autonomous_orchestrator import AutonomousOrchestrator


app = FastAPI(
    title="FREE BASICS AI MARKETING SYSTEM"
)


# =========================
# DATA LAYER
# =========================

sheets = SheetsEngine()


# =========================
# AI CORE
# =========================

ai = AICoreEngine(
    sheets
)


# =========================
# CONTENT
# =========================

content = ContentAI()


# =========================
# MONEY
# =========================

revenue = RevenueEngine()


# =========================
# LEARNING
# =========================

learning = AILearningLoop(
    sheets,
    revenue
)


# =========================
# SAFE PUBLISHERS
# =========================

class SafeYouTube:

    def upload(
        self,
        file_path,
        title,
        description
    ):

        return {
            "status": "waiting_for_video_asset"
        }



class SafePinterest:

    def create_pin(
        self,
        board_id,
        title,
        link,
        image_url
    ):

        return {
            "status": "waiting_for_image_asset"
        }



youtube = SafeYouTube()

pinterest = SafePinterest()


# =========================
# AUTOPILOT
# =========================

autopilot = AutopilotOrchestrator(
    ai,
    content,
    sheets,
    youtube,
    pinterest,
    revenue
)


system = AutonomousOrchestrator(
    autopilot,
    learning
)


trigger = CloudSchedulerTrigger(
    system
)


# =========================
# HOME API
# =========================

@app.get("/")
def home():

    return {
        "system": "FREE BASICS",
        "phase": "CONNECTED",
        "status": "READY"
    }



# =========================
# PINTEREST DOMAIN VERIFICATION
# =========================

@app.get(
    "/pinterest-verification",
    response_class=HTMLResponse
)
def pinterest_verification():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="p:domain_verify" content="bc27656eea0774520fbe08d0a275427d"/>
        <title>Free Basics</title>
    </head>
    <body>
        Free Basics
    </body>
    </html>
    """



# =========================
# AI RUN
# =========================

@app.post("/run")
def run_system():

    return trigger.execute()
