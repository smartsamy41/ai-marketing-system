class MoneyEngineV2:

    def __init__(self):

        self.data = {
            "energie": {"clicks": 0, "leads": 0, "revenue": 0},
            "finanzen": {"clicks": 0, "leads": 0, "revenue": 0},
            "tech": {"clicks": 0, "leads": 0, "revenue": 0}
        }

    # =========================
    # CLICK TRACKING
    # =========================
    def track_click(self, category):

        if category in self.data:
            self.data[category]["clicks"] += 1

    # =========================
    # LEAD TRACKING
    # =========================
    def track_lead(self, category, value=1.0):

        if category in self.data:
            self.data[category]["leads"] += 1
            self.data[category]["revenue"] += value

    # =========================
    # REVENUE SCORE (CORE AI SIGNAL)
    # =========================
    def revenue_score(self, category):

        d = self.data.get(category, {})

        clicks = d.get("clicks", 0)
        leads = d.get("leads", 0)
        revenue = d.get("revenue", 0)

        if clicks == 0:
            return 0

        return (revenue * 10) + (leads * 5) + clicks

    # =========================
    # BEST CATEGORY DETECTOR
    # =========================
    def best_category(self):

        scores = {}

        for cat in self.data.keys():
            scores[cat] = self.revenue_score(cat)

        best = max(scores, key=scores.get)

        return {
            "best_category": best,
            "scores": scores
        }

    # =========================
    # AI PRIORITY SIGNAL (FOR AUTOPILOT)
    # =========================
    def priority_signal(self):

        best = self.best_category()["best_category"]

        return {
            "focus": best,
            "instruction": f"BOOST {best.upper()} CONTENT"
        }
