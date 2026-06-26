from datetime import datetime


class AutoScalingEngine:

    def __init__(self):

        self.history = []
        self.product_scores = {}

    # =========================
    # UPDATE METRICS
    # =========================
    def update_metrics(self, product_id, clicks=0, views=0, revenue=0):

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

        return self.product_scores[product_id]

    # =========================
    # SCORING SYSTEM
    # =========================
    def calculate_score(self, product_id):

        data = self.product_scores.get(product_id, {})

        clicks = data.get("clicks", 0)
        views = data.get("views", 0)
        revenue = data.get("revenue", 0)

        # 🔥 weighting logic (IMPORTANT)
        score = (clicks * 2.0) + (views * 0.5) + (revenue * 10.0)

        self.product_scores[product_id]["score"] = score

        return score

    # =========================
    # BEST PRODUCT DETECTION
    # =========================
    def get_best_product(self):

        best_product = None
        best_score = -1

        for pid in self.product_scores:

            score = self.calculate_score(pid)

            if score > best_score:
                best_score = score
                best_product = pid

        return {
            "best_product": best_product,
            "best_score": best_score
        }

    # =========================
    # SCALING DECISION ENGINE
    # =========================
    def scaling_decision(self):

        best = self.get_best_product()

        if not best["best_product"]:

            return {
                "status": "NO_DATA"
            }

        decision = {
            "timestamp": datetime.utcnow().isoformat(),
            "best_product": best["best_product"],
            "score": best["best_score"],

            "action": {
                "scale_up": best["best_product"],
                "scale_down_candidates": self._get_low_performers()
            }
        }

        self.history.append(decision)

        return decision

    # =========================
    # LOW PERFORMERS
    # =========================
    def _get_low_performers(self):

        low = []

        for pid, data in self.product_scores.items():

            if data.get("score", 0) < 10:
                low.append(pid)

        return low

    # =========================
    # EXECUTE SCALING (LOGIC ONLY)
    # =========================
    def execute_scaling(self):

        decision = self.scaling_decision()

        return {
            "status": "SCALING_EXECUTED",
            "decision": decision
        }
