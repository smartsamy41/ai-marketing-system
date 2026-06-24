from datetime import datetime


class ScalingEngine:

    def __init__(self, revenue_engine=None, traffic_engine=None, tracking_engine=None):
        self.revenue_engine = revenue_engine
        self.traffic_engine = traffic_engine
        self.tracking_engine = tracking_engine

    # =========================
    # SAFE CALL HELPER
    # =========================
    def safe_call(self, func, default):
        try:
            if func:
                return func()
        except Exception as e:
            return {"error": str(e)}
        return default

    # =========================
    # ANALYZE SYSTEM
    # =========================
    def analyze(self):

        traffic = self.safe_call(
            lambda: self.traffic_engine.get_stats(),
            {}
        )

        tracking = self.safe_call(
            lambda: self.tracking_engine.get_summary(),
            {}
        )

        revenue = self.safe_call(
            lambda: self.revenue_engine.run_cycle(),
            {}
        )

        # =========================
        # SAFE VALUE EXTRACTION
        # =========================
        try:
            clicks = int(tracking.get("clicks", 0) or 0)
        except:
            clicks = 0

        try:
            conversions = int(tracking.get("conversions", 0) or 0)
        except:
            conversions = 0

        try:
            revenue_value = float(
                revenue.get("metrics", {}).get("revenue", 0) or 0
            )
        except:
            revenue_value = 0.0

        score = clicks * 0.1 + conversions * 5 + revenue_value * 0.01

        return {
            "status": "ANALYSIS_DONE",
            "metrics": {
                "traffic": traffic,
                "tracking": tracking,
                "revenue": revenue
            },
            "score": round(score, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # DECISION ENGINE
    # =========================
    def decide(self):

        analysis = self.analyze()
        score = analysis.get("score", 0)

        if score > 80:
            action = "SCALE"
        elif score > 40:
            action = "BOOST"
        else:
            action = "OPTIMIZE"

        return {
            "status": "DECISION_MADE",
            "action": action,
            "score": score,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # RUN CYCLE
    # =========================
    def run(self):

        return {
            "status": "SCALING_CYCLE_COMPLETE",
            "analysis": self.analyze(),
            "decision": self.decide()
        }
