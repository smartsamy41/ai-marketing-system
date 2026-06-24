from datetime import datetime


# =========================
# MASTER AUTOPILOT ENGINE
# =========================
class MasterAutopilotEngine:

    def __init__(self, revenue_engine, email_engine, tracking_engine):

        self.revenue_engine = revenue_engine
        self.email_engine = email_engine
        self.tracking_engine = tracking_engine

    # =========================
    # RUN FULL SYSTEM CYCLE
    # =========================
    def run(self):

        revenue = self.revenue_engine.run_cycle()
        email_campaign = self.email_engine.run_campaign()
        summary = self.tracking_engine.get_summary()

        return {
            "status": "MASTER_CYCLE_COMPLETE",
            "timestamp": datetime.utcnow().isoformat(),
            "revenue": revenue,
            "email_campaign": email_campaign,
            "tracking": summary
        }

    # =========================
    # LIVE DECISION ENGINE
    # =========================
    def decision(self):

        summary = self.tracking_engine.get_summary()

        clicks = summary.get("clicks", 0)
        conversions = summary.get("conversions", 0)
        revenue = summary.get("revenue", 0)

        score = clicks * 0.1 + conversions * 5 + revenue * 0.01

        if score > 50:
            action = "SCALE"
        elif score > 20:
            action = "BOOST"
        else:
            action = "OPTIMIZE"

        return {
            "status": "DECISION_COMPLETE",
            "action": action,
            "score": round(score, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # AUTOPILOT LOOP (CORE)
    # =========================
    def loop(self):

        return {
            "status": "AUTOPILOT_LOOP_RUNNING",
            "cycle": self.run(),
            "decision": self.decision()
        }
