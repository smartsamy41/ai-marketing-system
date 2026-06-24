from datetime import datetime

class V12BusinessOS:

    def __init__(self, v11_engine, v10_engine, scaling_engine):

        self.v11 = v11_engine
        self.v10 = v10_engine
        self.scaling = scaling_engine

        self.memory = []
        self.decisions = []

    # =========================
    # COLLECT FULL SYSTEM DATA
    # =========================
    def collect(self, product_id):

        cloud = self.v11.run_cloud_cycle(product_id)
        score = self.scaling.analyze_product(product_id)
        money = self.v10.analyze()

        snapshot = {
            "product_id": product_id,
            "cloud": cloud,
            "score": score,
            "money": money,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.memory.append(snapshot)

        return snapshot

    # =========================
    # BUSINESS DECISION ENGINE
    # =========================
    def decide(self):

        if not self.memory:
            return {"action": "NO_DATA"}

        latest = self.memory[-1]

        revenue = latest["money"].get("revenue", 0)
        score = latest["score"].get("score", 0)

        if revenue > 200 and score > 80:
            action = "SCALE_AGGRESSIVE"
        elif revenue > 100:
            action = "SCALE"
        elif score > 40:
            action = "OPTIMIZE"
        else:
            action = "REBUILD_STRATEGY"

        decision = {
            "action": action,
            "revenue": revenue,
            "score": score,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.decisions.append(decision)

        return decision

    # =========================
    # EXECUTION LAYER
    # =========================
    def execute(self, product_id):

        decision = self.decide()

        if decision["action"] == "SCALE_AGGRESSIVE":
            result = self.v11.scheduler_run(["CHK24_001", "TC_001", "AMZ_001"])
        elif decision["action"] == "SCALE":
            result = self.v11.run_cloud_cycle(product_id)
        else:
            result = self.v11.run_cloud_cycle(product_id)

        return {
            "status": "EXECUTED",
            "decision": decision,
            "result": result
        }

    # =========================
    # FULL CYCLE
    # =========================
    def run(self, product_id):

        self.collect(product_id)
        execution = self.execute(product_id)

        return {
            "status": "V12_BUSINESS_CYCLE_DONE",
            "execution": execution
        }

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "memory_size": len(self.memory),
            "decisions": len(self.decisions),
            "last_decision": self.decisions[-1] if self.decisions else None
        }
