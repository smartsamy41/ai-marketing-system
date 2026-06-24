from datetime import datetime


# =========================
# AUTOPILOT CONNECTOR (MASTER ORCHESTRATION)
# =========================
class AutopilotConnector:

    def __init__(self, orchestrator, pipeline, email_engine, tracking, revenue_engine):

        self.orchestrator = orchestrator
        self.pipeline = pipeline
        self.email_engine = email_engine
        self.tracking = tracking
        self.revenue_engine = revenue_engine

    # =========================
    # RUN FULL AUTOPILOT CYCLE
    # =========================
    def run_cycle(self, product_id, category="default"):

        # 1. ORCHESTRATOR
        job = {
            "product_id": product_id,
            "category": category,
            "data": {}
        }

        orch_result = None

        try:
            orch_result = self.orchestrator(job)
        except Exception as e:
            orch_result = {"error": str(e)}

        # 2. CONTENT PIPELINE
        content = self.pipeline.run(product_id)

        # 3. TRACKING CLICK SIMULATION
        click = self.tracking.track_click(product_id, source="autopilot")

        # 4. EMAIL CAMPAIGN (OPTIONAL)
        campaign = self.email_engine.run_campaign()

        # 5. REVENUE ANALYSIS
        revenue = self.revenue_engine.run_cycle()

        # =========================
        # FINAL RESULT
        # =========================
        return {
            "status": "AUTOPILOT_CYCLE_DONE",
            "timestamp": str(datetime.utcnow()),
            "orchestrator": orch_result,
            "content": content,
            "click": click,
            "campaign": campaign,
            "revenue": revenue
        }
