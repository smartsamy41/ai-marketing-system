class AILearningEngine:

    def __init__(self, sheets_engine):
        self.sheets = sheets_engine

    # =========================
    # ANALYZE SYSTEM PERFORMANCE
    # =========================
    def analyze(self):

        data = self.sheets.export_data()

        clicks = data.get("clicks", [])
        conversions = data.get("conversions", [])

        # -------------------------
        # CLICK ANALYSIS
        # -------------------------
        product_scores = {}

        for c in clicks:
            product = c.get("product")
            if product:
                product_scores[product] = product_scores.get(product, 0) + 1

        # -------------------------
        # REVENUE CALCULATION
        # -------------------------
        revenue = 0.0

        for conv in conversions:
            revenue += conv.get("value", 0)

        # -------------------------
        # SORT TOP PRODUCTS
        # -------------------------
        sorted_products = sorted(
            product_scores.items(),
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
    # AI RECOMMENDATION SYSTEM
    # =========================
    def suggest(self):

        analysis = self.analyze()

        if analysis["total_clicks"] == 0:
            return {
                "status": "no_data",
                "message": "No clicks available yet"
            }

        top_products = analysis["top_products"]

        if not top_products:
            return {
                "status": "no_products_found"
            }

        best_product = top_products[0][0]

        return {
            "status": "ok",
            "best_product": best_product,
            "reason": "highest click performance",
            "revenue": analysis["revenue"]
        }
