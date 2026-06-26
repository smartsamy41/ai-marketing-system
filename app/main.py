from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "OK",
        "system": "ORCHESTRATOR LAZY MODE"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/run")
def run():
    try:
        from engine.orchestrator_clean_master import OrchestratorCleanMaster

        orchestrator = OrchestratorCleanMaster()
        return orchestrator.run_all(None)

    except Exception as e:
        return {
            "status": "FAILED_SAFE",
            "error": str(e),
            "note": "Cloud bleibt online. Fehler liegt im Orchestrator oder Engine Import."
        }
