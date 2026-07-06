class AILearningLoop:

    def __init__(self, sheets, revenue_engine):

        self.sheets = sheets
        self.revenue = revenue_engine

    # =========================
    # ANALYZE SYSTEM PERFORMANCE
    # =========================
    def analyze(self):

        data = self.sheets.export()

        clicks = data["clicks"]
        conversions = data["conversions"]

        product_score = {}

        for c in clicks:
            p = c["product"]
            product_score[p] = product_score.get(p, 0) + 1

        best_product = max(product_score, key=product_score.get) if product_score else None

        return {
            "best_product": best_product,
            "total_clicks": len(clicks),
            "total_conversions": len(conversions)
        }

    # =========================
    # OPTIMIZATION DECISION
    # =========================
    def optimize(self):

        analysis = self.analyze()

        if not analysis["best_product"]:
            return {"status": "no_data"}

        return {
            "action": "BOOST_PRODUCT",
            "product": analysis["best_product"]
        }
