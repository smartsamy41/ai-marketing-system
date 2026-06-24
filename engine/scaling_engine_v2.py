from datetime import datetime


class ScalingEngine:

    def __init__(self, revenue_engine=None, traffic_engine=None, tracking_engine=None):

        self.revenue_engine = revenue_engine
        self.traffic_engine = traffic_engine
        self.tracking_engine = tracking_engine

    # =========================
    # ANALYSIS (SAFE MODE)
    # =========================
    def analyze(self):

        traffic = {}
        tracking = {}
        revenue = {}

        try:
            if self.traffic_engine:
                traffic = self.traffic_engine.get_stats()
        except Exception as e:
            traffic = {"error": str(e)}

        try:
            if self.tracking_engine:
                tracking = self.tracking_engine.get_summary()
        except Exception as e:
            tracking = {"error": str(e)}

        try:
            if self.revenue_engine:
                revenue = self.revenue_engine.run_cycle()
        except Exception as e:
            revenue = {"error": str(e)}

        clicks = tracking.get("clicks", 0)
        conversions = tracking.get("conversions", 0)

        revenue_value = 0
        try:
            revenue_value = revenue.get("metrics", {}).get("revenue", 0)
        except:
            revenue_value = 0

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
            "score": score
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
