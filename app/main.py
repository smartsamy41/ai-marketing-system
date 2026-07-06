from fastapi import FastAPI

from engine.cloud_scheduler_trigger import CloudSchedulerTrigger
from engine.secret_manager import SecretManager

from engine.sheets_engine import SheetsEngine
from engine.ai_core_engine import AICoreEngine
from engine.content_ai import ContentAI

from engine.revenue_engine import RevenueEngine

from engine.ai_learning_engine import AILearningLoop

from engine.autopilot_orchestrator import AutopilotOrchestrator
from engine.autonomous_orchestrator import AutonomousOrchestrator


app = FastAPI(title="FREE BASICS AI MARKETING SYSTEM")


# =========================
# CORE SERVICES
# =========================

secrets = SecretManager()


# DATA LAYER

sheets = SheetsEngine()


# AI

ai = AICoreEngine(
    sheets
)


# CONTENT

content = ContentAI()


# MONEY

revenue = RevenueEngine()


# LEARNING

learning = AILearningLoop(
    sheets,
    revenue
)


# =========================
# SAFE PUBLISH PLACEHOLDERS
# =========================

class SafeYouTube:

    def upload(
        self,
        file_path,
        title,
        description
    ):

        return {
            "status": "waiting_for_youtube_asset"
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
            "status": "waiting_for_pinterest_asset"
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
# HEALTH
# =========================

@app.get("/")
def home():

    return {

        "system": "FREE BASICS",

        "phase": "PRODUCTION CONNECTED",

        "status": "READY"

    }



# =========================
# AI CYCLE
# =========================

@app.post("/run")
def run_system():

    return trigger.execute()
