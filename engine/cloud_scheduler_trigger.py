class CloudSchedulerTrigger:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

    # =========================
    # ENTRY POINT (Cloud Run Trigger)
    # =========================
    def execute(self):

        result = self.orchestrator.run()

        return {
            "status": "EXECUTED",
            "result": result
        }
