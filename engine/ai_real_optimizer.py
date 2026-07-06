class AIRealOptimizer:

    def __init__(self, sheets):

        self.sheets = sheets

    # =========================
    # REAL DATA ANALYSIS
    # =========================
    def analyze(self, clicks, conversions):

        score = {}

        for c in clicks:
            p = c[0]
            score[p] = score.get(p, 0) + 1

        revenue = sum([c[1] for c in conversions if isinstance(c[1], (int, float))])

        return {
            "score": score,
            "revenue": revenue
        }

    # =========================
    # PICK BEST PRODUCT
    # =========================
    def pick_best(self, clicks, conversions):

        analysis = self.analyze(clicks, conversions)

        if not analysis["score"]:
            return None

        best = max(analysis["score"], key=analysis["score"].get)

        return best
