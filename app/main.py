from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "step": "1"}

@app.get("/health")
def health():
    return {"status": "OK", "step": "2"}

@app.get("/run")
def run():
    try:
        from engine.orchestrator_clean_master import OrchestratorCleanMaster

        o = OrchestratorCleanMaster()
        return o.run_all()

    except Exception as e:
        return {
            "status": "CRASH_DETECTED",
            "error": str(e),
            "step": "ORCHESTRATOR_IMPORT_FAILED"
        }
