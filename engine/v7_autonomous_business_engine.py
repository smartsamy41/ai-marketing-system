from datetime import datetime

class V7AutonomousBusiness:

    def __init__(self, v6_engine, scaling_engine, conversion_engine):

        self.v6 = v6_engine
        self.scaling = scaling_engine
        self.conversion = conversion_engine

        self.business_memory = []
        self.actions_log = []

    # =========================
    # OBSERVE FULL BUSINESS
    # =========================
    def observe(self, products):

        v6_state = self.v6.run(products)
        report = self.v6.report()

        snapshot = {
            "v6_state": v6_state,
            "report": report,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.business_memory.append(snapshot)

        return snapshot

    # =========================
    # BUSINESS DECISION ENGINE
    # =========================
    def decide(self):

        if not self.business_memory:
            return {"action": "NO_DATA"}

        latest = self.business_memory[-1]
        report = latest["report"]

        # =========================
        # BUSINESS LOGIC
        # =========================
        if report["total_cycles"] > 10 and report["evolution_steps"] > 5:
            action = "SCALE_MARKETING"
        elif report["total_cycles"] > 5:
            action = "OPTIMIZE_FUNNELS"
        else:
            action = "BUILD_TRAFFIC"

        decision = {
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "report": report
        }

        self.actions_log.append(decision)

        return decision

    # =========================
    # EXECUTE BUSINESS ACTION
    # =========================
    def execute(self, products):

        decision = self.decide()

        execution = {
            "decision": decision,
            "products": products,
            "timestamp": datetime.utcnow().isoformat()
        }

        return execution

    # =========================
    # FULL BUSINESS LOOP
    # =========================
    def run(self, products):

        observation = self.observe(products)
        execution = self.execute(products)

        return {
            "status": "V7_BUSINESS_CYCLE_DONE",
            "observation": observation,
            "execution": execution
        }

    # =========================
    # BUSINESS REPORT
    # =========================
    def report(self):

        return {
            "memory_size": len(self.business_memory),
            "actions": len(self.actions_log),
            "last_action": self.actions_log[-1] if self.actions_log else None
        }
