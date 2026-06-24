from datetime import datetime


# =========================
# SCALING ENGINE (AUTONOMOUS GROWTH)
# =========================
class ScalingEngine:

    def __init__(self, revenue_engine, traffic_engine, tracking_engine):

        self.revenue_engine = revenue_engine
        self.traffic_engine = traffic_engine
        self.tracking_engine = tracking_engine

    # =========================
    # ANALYZE SYSTEM HEALTH
    # =========================
    def analyze(self):

        revenue = self.revenue_engine.run_cycle()
        traffic = self.traffic_engine.get_stats()
        tracking = self.tracking_engine.get_summary()

        score = (
            traffic.get("conversion_rate", 0) * 100 +
            tracking.get("clicks", 0) * 0.1 +
            tracking.get("conversions", 0) * 5 +
            revenue.get("metrics", {}).get("revenue", 0) * 0.01
        )

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
        score = analysis["score"]

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
    # EXECUTE SCALE LOOP
    # =========================
    def run(self):

        return {
            "status": "SCALING_CYCLE_COMPLETE",
            "analysis": self.analyze(),
            "decision": self.decide()
        }
