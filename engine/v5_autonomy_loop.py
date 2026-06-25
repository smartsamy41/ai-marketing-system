from datetime import datetime

class AutonomyLoopV5:

    def __init__(self):
        self.state = {
            "traffic": 0,
            "clicks": 0,
            "leads": 0,
            "revenue": 0
        }

    # =========================
    # STEP 1: COLLECT DATA
    # =========================
    def collect(self, traffic, clicks, leads, revenue):

        self.state["traffic"] += traffic
        self.state["clicks"] += clicks
        self.state["leads"] += leads
        self.state["revenue"] += revenue

        return self.state

    # =========================
    # STEP 2: DECISION ENGINE
    # =========================
    def decide(self):

        if self.state["clicks"] == 0:
            return {
                "action": "WAIT",
                "reason": "NO_DATA"
            }

        cr = self.state["leads"] / self.state["clicks"]

        if self.state["revenue"] > 20:
            action = "SCALE"
        elif cr > 0.3:
            action = "OPTIMIZE"
        elif cr > 0:
            action = "TEST_NEW_CONTENT"
        else:
            action = "REBUILD_FLOW"

        return {
            "action": action,
            "conversion_rate": cr,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # STEP 3: RESET CYCLE
    # =========================
    def reset(self):

        self.state = {
            "traffic": 0,
            "clicks": 0,
            "leads": 0,
            "revenue": 0
        }

        return {"status": "RESET_DONE"}
