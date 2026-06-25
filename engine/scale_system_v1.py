from datetime import datetime

class ScaleSystemV1:

    def __init__(self):
        self.metrics = {
            "traffic": 0,
            "clicks": 0,
            "leads": 0,
            "revenue": 0
        }

    # =========================
    # INPUT UPDATE
    # =========================
    def update(self, traffic=0, clicks=0, leads=0, revenue=0):

        self.metrics["traffic"] += traffic
        self.metrics["clicks"] += clicks
        self.metrics["leads"] += leads
        self.metrics["revenue"] += revenue

        return {
            "status": "UPDATED",
            "metrics": self.metrics
        }

    # =========================
    # SCALING DECISION ENGINE
    # =========================
    def decision(self):

        if self.metrics["revenue"] > 0 and self.metrics["clicks"] > 0:

            cr = self.metrics["leads"] / self.metrics["clicks"] if self.metrics["clicks"] > 0 else 0
            roi = self.metrics["revenue"]

            if roi > 10:
                action = "SCALE_UP"
            elif roi > 0:
                action = "OPTIMIZE"
            else:
                action = "REDUCE"

        else:
            cr = 0
            action = "COLLECT_DATA"

        return {
            "status": "DECISION_MADE",
            "action": action,
            "conversion_rate": cr,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # RESET CYCLE
    # =========================
    def reset(self):

        self.metrics = {
            "traffic": 0,
            "clicks": 0,
            "leads": 0,
            "revenue": 0
        }

        return {"status": "RESET_DONE"}
