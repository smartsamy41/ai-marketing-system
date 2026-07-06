class AIFeedbackLoop:

    def __init__(self, tracking):

        self.tracking = tracking

    def optimize(self):

        clicks = self.tracking.clicks
        conversions = self.tracking.conversions

        score = {}

        for c in clicks:
            score[c] = score.get(c, 0) + 1

        best = max(score, key=score.get) if score else None

        return {
            "best_product": best,
            "total_clicks": len(clicks),
            "revenue": self.tracking.revenue()
        }
