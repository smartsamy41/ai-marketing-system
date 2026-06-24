from datetime import datetime

class V5AutonomyEngine:

    def __init__(self, scaling_engine, conversion_engine):

        self.scaling_engine = scaling_engine
        self.conversion_engine = conversion_engine
        self.memory = []

    # =========================
    # OBSERVE SYSTEM
    # =========================
    def observe(self, product_id):

        score = self.conversion_engine.product_score(product_id)
        decision = self.scaling_engine.analyze_product(product_id)

        state = {
            "product_id": product_id,
            "score": score,
            "decision": decision,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.memory.append(state)

        return state

    # =========================
    # LEARNING ENGINE
    # =========================
    def learn(self):

        total = len(self.memory)

        scale = len([m for m in self.memory if m["decision"]["decision"] == "SCALE"])
        boost = len([m for m in self.memory if m["decision"]["decision"] == "BOOST"])
        stop = len([m for m in self.memory if m["decision"]["decision"] == "STOP"])

        return {
            "total_events": total,
            "scale_ratio": scale / total if total else 0,
            "boost_ratio": boost / total if total else 0,
            "stop_ratio": stop / total if total else 0
        }

    # =========================
    # AUTONOMOUS DECISION ENGINE
    # =========================
    def decide_next_action(self):

        learning = self.learn()

        if learning["scale_ratio"] > 0.5:
            action = "EXPAND_SCALE"
        elif learning["boost_ratio"] > 0.3:
            action = "OPTIMIZE"
        else:
            action = "REBALANCE"

        return {
            "action": action,
            "learning": learning,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # FULL CYCLE
    # =========================
    def run_cycle(self, products):

        observations = []

        for p in products:
            observations.append(self.observe(p))

        return {
            "status": "V5_CYCLE_DONE",
            "observations": observations,
            "decision": self.decide_next_action()
        }
