class MoneyEngineV4:

    def __init__(self):

        self.data = {
            "energie": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "finanzen": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "tech": {"clicks": 0, "leads": 0, "revenue": 0.0}
        }

        self.blocked = set()
        self.boost_factor = {}

    # =========================
    # CLICK TRACKING
    # =========================
    def track_click(self, category: str):

        if category in self.blocked:
            return

        self.data[category]["clicks"] += 1

    # =========================
    # LEAD TRACKING (REAL MONEY)
    # =========================
    def track_lead(self, category: str, value: float = 1.0):

        if category in self.blocked:
            return

        self.data[category]["leads"] += 1
        self.data[category]["revenue"] += value

    # =========================
    # REVENUE INTELLIGENCE SCORE
    # =========================
    def score(self, category: str):

        d = self.data.get(category, {})

        clicks = d.get("clicks", 0)
        leads = d.get("leads", 0)
        revenue = d.get("revenue", 0.0)

        if clicks == 0:
            return 0

        # aggressive weighting: revenue dominates
        return (revenue * 25) + (leads * 10) + clicks

    # =========================
    # AUTO BLOCKING SYSTEM
    # =========================
    def auto_block(self):

        for cat, data in self.data.items():

            if data["clicks"] > 20 and data["revenue"] == 0:
                self.blocked.add(cat)

        return list(self.blocked)

    # =========================
    # BOOST SYSTEM
    # =========================
    def boost(self):

        scores = {c: self.score(c) for c in self.data}

        best = max(scores, key=scores.get)

        self.boost_factor = {
            best: 1.0,
            **{k: round(v / (sum(scores.values()) or 1), 2) for k, v in scores.items()}
        }

        return {
            "best_category": best,
            "boost_map": self.boost_factor
        }

    # =========================
    # CONTENT PRIORITY ENGINE
    # =========================
    def content_priority(self):

        boost_data = self.boost()

        return {
            "focus": boost_data["best_category"],
            "instruction": f"PRIORITIZE {boost_data['best_category'].upper()} CONTENT",
            "distribution": boost_data["boost_map"]
        }

    # =========================
    # FULL AUTONOMOUS DECISION
    # =========================
    def decision(self):

        blocked = self.auto_block()
        boost = self.boost()
        priority = self.content_priority()

        return {
            "status": "V4_ACTIVE",
            "best_category": boost["best_category"],
            "blocked_categories": blocked,
            "boost": boost["boost_map"],
            "priority": priority
        }
