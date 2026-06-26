from datetime import datetime


class AILearningLoop:

    def __init__(self):

        self.logs = []
        self.product_stats = {}

    # =========================
    # LOG EVENT
    # =========================
    def log_event(self, product_id, event_type, value=1):

        if product_id not in self.product_stats:

            self.product_stats[product_id] = {
                "clicks": 0,
                "views": 0,
                "revenue": 0,
                "videos": 0
            }

        if event_type == "click":
            self.product_stats[product_id]["clicks"] += value

        elif event_type == "view":
            self.product_stats[product_id]["views"] += value

        elif event_type == "revenue":
            self.product_stats[product_id]["revenue"] += value

        elif event_type == "video":
            self.product_stats[product_id]["videos"] += value

        self.logs.append({
            "product_id": product_id,
            "event": event_type,
            "value": value,
            "time": datetime.utcnow().isoformat()
        })

        return self.product_stats[product_id]

    # =========================
    # SCORE CALCULATION
    # =========================
    def calculate_score(self, product_id):

        stats = self.product_stats.get(product_id, {})

        clicks = stats.get("clicks", 0)
        views = stats.get("views", 0)
        revenue = stats.get("revenue", 0)

        score = (clicks * 1.0) + (views * 0.3) + (revenue * 10)

        return {
            "product_id": product_id,
            "score": score,
            "stats": stats
        }

    # =========================
    # BEST PRODUCT SELECTION
    # =========================
    def get_best_product(self):

        best = None
        best_score = -1

        for pid in self.product_stats:

            result = self.calculate_score(pid)

            if result["score"] > best_score:

                best_score = result["score"]
                best = result

        return best

    # =========================
    # OPTIMIZATION ACTION
    # =========================
    def optimize(self):

        best = self.get_best_product()

        if not best:
            return {
                "status": "NO_DATA"
            }

        return {
            "status": "OPTIMIZATION_DONE",
            "best_product": best,
            "recommendation": f"Scale {best['product_id']} and reduce low performers"
        }
