from datetime import datetime


class AdsOptimizationEngine:

    def __init__(self):

        self.product_scores = {}

    # =========================
    # FEED DATA
    # =========================
    def feed(self, product_id, clicks=0, views=0, revenue=0):

        if product_id not in self.product_scores:

            self.product_scores[product_id] = {
                "clicks": 0,
                "views": 0,
                "revenue": 0,
                "score": 0
            }

        self.product_scores[product_id]["clicks"] += clicks
        self.product_scores[product_id]["views"] += views
        self.product_scores[product_id]["revenue"] += revenue

    # =========================
    # SCORE CALCULATION
    # =========================
    def calculate_score(self, product_id):

        data = self.product_scores.get(product_id, {})

        score = (
            data.get("clicks", 0) * 2 +
            data.get("views", 0) * 0.5 +
            data.get("revenue", 0) * 10
        )

        self.product_scores[product_id]["score"] = score

        return score

    # =========================
    # BEST PRODUCT
    # =========================
    def get_best(self):

        best = None
        best_score = -1

        for pid in self.product_scores:

            s = self.calculate_score(pid)

            if s > best_score:
                best_score = s
                best = pid

        return {
            "best_product": best,
            "score": best_score
        }

    # =========================
    # OPTIMIZATION DECISION
    # =========================
    def optimize(self):

        best = self.get_best()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "BOOST_TOP_PRODUCT",
            "best_product": best["best_product"],
            "strategy": "increase_content_frequency + video_priority + landingpage_boost"
        }
