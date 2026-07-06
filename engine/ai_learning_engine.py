class AILearningEngine:

    def __init__(self, sheets_engine):

        self.sheets = sheets_engine

    # =========================
    # ANALYZE PERFORMANCE
    # =========================
    def analyze(self):

        data = self.sheets.export_data()

        clicks = data["clicks"]
        conversions = data["conversions"]

        product_score = {}

        # CLICK ANALYSIS
        for c in clicks:
            p = c["product"]
            product_score[p] = product_score.get(p, 0) + 1

        # REVENUE CALCULATION
        revenue = 0
        for conv in conversions:
            revenue += conv["value"]

        # TOP PRODUCTS SORTING
        sorted_products = sorted(
            product_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "total_clicks": len(clicks),
            "total_conversions": len(conversions),
            "revenue": revenue,
            "top_products": sorted_products
        }

    # =========================
    # SIMPLE OPTIMIZATION SUGGESTION
    # =========================
    def suggest(self):

        analysis = self.analyze()

        if analysis["total_clicks"] == 0:
            return "No data yet"

        top = analysis["top_products"]

        if top:
            return {
                "best_product": top[0][0],
                "reason": "highest click rate"
            }

        return {"status": "insufficient data"}
