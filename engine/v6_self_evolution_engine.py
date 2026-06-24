from datetime import datetime
import copy

class V6SelfEvolutionEngine:

    def __init__(self, v5_engine, scaling_engine, conversion_engine):

        self.v5 = v5_engine
        self.scaling = scaling_engine
        self.conversion = conversion_engine

        self.strategy_memory = []
        self.evolution_log = []

    # =========================
    # OBSERVE SYSTEM STATE
    # =========================
    def observe(self, products):

        state = self.v5.run_cycle(products)
        learning = self.v5.learn()

        snapshot = {
            "state": state,
            "learning": learning,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.strategy_memory.append(snapshot)

        return snapshot

    # =========================
    # EVOLUTION DECISION ENGINE
    # =========================
    def decide_evolution(self):

        if not self.strategy_memory:
            return {"action": "NO_DATA"}

        latest = self.strategy_memory[-1]
        learning = latest["learning"]

        # =========================
        # EVOLUTION LOGIC
        # =========================
        if learning["scale_ratio"] > 0.6:
            action = "AGGRESSIVE_SCALE"
        elif learning["boost_ratio"] > 0.4:
            action = "OPTIMIZE_FUNNEL"
        elif learning["stop_ratio"] > 0.5:
            action = "CLEAN_NON_PERFORMERS"
        else:
            action = "STABLE_RUN"

        decision = {
            "action": action,
            "learning": learning,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.evolution_log.append(decision)

        return decision

    # =========================
    # SELF IMPROVEMENT STEP
    # =========================
    def evolve(self):

        decision = self.decide_evolution()

        # safe "strategy mutation" (NO CRASH, ONLY LOGIC)
        new_strategy = copy.deepcopy(decision)

        return {
            "status": "EVOLUTION_STEP_DONE",
            "decision": decision,
            "strategy": new_strategy
        }

    # =========================
    # FULL CYCLE
    # =========================
    def run(self, products):

        observation = self.observe(products)
        evolution = self.evolve()

        return {
            "status": "V6_CYCLE_DONE",
            "observation": observation,
            "evolution": evolution
        }

    # =========================
    # SYSTEM INTELLIGENCE REPORT
    # =========================
    def report(self):

        return {
            "total_cycles": len(self.strategy_memory),
            "evolution_steps": len(self.evolution_log),
            "latest_action": self.evolution_log[-1] if self.evolution_log else None
        }
