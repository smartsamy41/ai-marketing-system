class MoneyEngineV5:

    def __init__(self):

        self.data = {
            "energie": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "finanzen": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "tech": {"clicks": 0, "leads": 0, "revenue": 0.0}
        }

        self.blocked = set()
        self.repair_mode = {}
        self.history = []

    # =========================
    # TRACK CLICK
    # =========================
    def track_click(self, category: str):

        if category in self.blocked:
            return

        self.data[category]["clicks"] += 1

    # =========================
    # TRACK LEAD
    # =========================
    def track_lead(self, category: str, value: float = 1.0):

        if category in self.blocked:
            return

        self.data[category]["leads"] += 1
        self.data[category]["revenue"] += value

    # =========================
    # REVENUE SCORE ENGINE
    # =========================
    def score(self, category: str):

        d = self.data.get(category, {})

        clicks = d.get("clicks", 0)
        leads = d.get("leads", 0)
        revenue = d.get("revenue", 0.0)

        if clicks == 0:
            return 0

        return (revenue * 30) + (leads * 12) + clicks

    # =========================
    # AUTO REPAIR SYSTEM
    # =========================
    def auto_repair(self):

        for cat, d in self.data.items():

            # DEAD FUNNEL DETECTION
            if d["clicks"] > 30 and d["revenue"] == 0:
                self.blocked.add(cat)
                self.repair_mode[cat] = "DEAD_FUNNEL"

            # LOW PERFORMANCE DETECTION
            if d["clicks"] > 10 and d["revenue"] < 2:
                self.repair_mode[cat] = "LOW_PERFORMANCE"

        return self.repair_mode

    # =========================
    # SELF OPTIMIZATION ENGINE
    # =========================
    def optimize(self):

        scores = {c: self.score(c) for c in self.data}

        best = max(scores, key=scores.get)

        total = sum(scores.values()) or 1

        distribution = {
            k: round(v / total, 2)
            for k, v in scores.items()
        }

        self.history.append({
            "best": best,
            "distribution": distribution
        })

        return {
            "best_category": best,
            "distribution": distribution
        }

    # =========================
    # CONTENT REALLOCATION ENGINE
    # =========================
    def reallocate(self):

        optimization = self.optimize()

        best = optimization["best_category"]

        return {
            "action": "REALLOCATE_TRAFFIC",
            "focus": best,
            "instruction": f"SHIFT ALL CONTENT TO {best.upper()}"
        }

    # =========================
    # FULL SELF-HEALING DECISION ENGINE
    # =========================
    def decision(self):

        repair = self.auto_repair()
        optimize = self.optimize()
        reallocate = self.reallocate()

        return {
            "status": "V5_SELF_HEALING_ACTIVE",
            "best_category": optimize["best_category"],
            "blocked": list(self.blocked),
            "repair_mode": repair,
            "distribution": optimize["distribution"],
            "action": reallocate
        }
