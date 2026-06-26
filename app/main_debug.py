from fastapi import FastAPI
from engine.orchestrator_clean_master import OrchestratorCleanMaster

# =========================
# APP
# =========================
app = FastAPI()

orchestrator = OrchestratorCleanMaster()

# =========================
# ROOT CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "LIVE_TEST_MODE",
        "system": "AI_MARKETING_DEBUG",
        "mode": "SAFE_CHECK"
    }

# =========================
# HEALTH CHECK (CRITICAL)
# =========================
@app.get("/health")
def health():
    return {
        "status": "OK",
        "ready": True,
        "orchestrator_loaded": True
    }

# =========================
# DEBUG RUN (STEP BY STEP)
# =========================
@app.get("/run")
def run():

    debug_log = {
        "step_1": "START",
        "step_2": None,
        "step_3": None,
        "step_4": None,
        "errors": None
    }

    try:
        debug_log["step_2"] = "CALL_ORCHESTRATOR"

        result = orchestrator.run_all()

        debug_log["step_3"] = "ORCHESTRATOR_DONE"
        debug_log["step_4"] = "SUCCESS"

        return {
            "status": "LIVE_TEST_SUCCESS",
            "debug": debug_log,
            "result_preview": {
                "product_count": len(result.get("results", [])),
                "mode": result.get("mode", "unknown")
            }
        }

    except Exception as e:

        debug_log["step_4"] = "FAILED"
        debug_log["errors"] = str(e)

        return {
            "status": "LIVE_TEST_FAILED",
            "debug": debug_log,
            "error": str(e)
        }
