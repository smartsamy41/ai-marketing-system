class MoneyEngineV3:

    def __init__(self):

        self.data = {
            "energie": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "finanzen": {"clicks": 0, "leads": 0, "revenue": 0.0},
            "tech": {"clicks": 0, "leads": 0, "revenue": 0.0}
        }

    # =========================
    # TRACK CLICK
    # =========================
    def track_click(self, category: str):

        if category in self.data:
            self.data[category]["clicks"] += 1

    # =========================
    # TRACK LEAD (REAL MONEY SIGNAL)
    # =========================
    def track_lead(self, category: str, value: float = 1.0):

        if category in self.data:
            self.data[category]["leads"] += 1
            self.data[category]["revenue"] += value

    # =========================
    # ROI SCORE (CORE INTELLIGENCE)
    # =========================
    def roi_score(self, category: str):

        d = self.data.get(category, {})

        clicks = d.get("clicks", 0)
        leads = d.get("leads", 0)
        revenue = d.get("revenue", 0.0)

        if clicks == 0:
            return 0

        # Gewichtung: Revenue > Leads > Clicks
        return (revenue * 20) + (leads * 8) + (clicks * 1)

    # =========================
    # BEST CATEGORY DETECTION
    # =========================
    def best_category(self):

        scores = {}

        for cat in self.data.keys():
            scores[cat] = self.roi_score(cat)

        best = max(scores, key=scores.get)

        return {
            "best_category": best,
            "scores": scores
        }

    # =========================
    # TRAFFIC BOOST DECISION ENGINE
    # =========================
    def boost_signals(self):

        best = self.best_category()["best_category"]

        return {
            "boost": best,
            "action": "INCREASE_CONTENT_WEIGHT",
            "instruction": f"FOCUS ALL SEO + CONTENT ON {best.upper()}"
        }

    # =========================
    # CONTENT WEIGHT SYSTEM
    # =========================
    def content_weights(self):

        scores = self.best_category()["scores"]

        total = sum(scores.values()) or 1

        weights = {}

        for k, v in scores.items():
            weights[k] = round(v / total, 2)

        return weights

    # =========================
    # FULL AI DECISION OUTPUT
    # =========================
    def decision(self):

        best = self.best_category()
        weights = self.content_weights()

        return {
            "best_category": best["best_category"],
            "weights": weights,
            "boost_instruction": self.boost_signals(),
            "status": "SELF_OPTIMIZING_ACTIVE"
        }
