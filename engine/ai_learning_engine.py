class AILearningLoop:

    def __init__(self, sheets, revenue_engine):

        self.sheets = sheets
        self.revenue = revenue_engine


    # =========================
    # ANALYZE PERFORMANCE
    # =========================

    def analyze(self):

        data = self.sheets.export()

        clicks = data.get("clicks", [])
        conversions = data.get("conversions", [])


        product_score = {}

        for click in clicks:

            product = click.get(
                "product",
                "unknown"
            )

            product_score[product] = (
                product_score.get(product, 0) + 1
            )


        best_product = None

        if product_score:

            best_product = max(
                product_score,
                key=product_score.get
            )


        revenue = 0

        for conversion in conversions:

            revenue += float(
                conversion.get("value", 0)
            )


        return {

            "best_product": best_product,

            "total_clicks": len(clicks),

            "total_conversions": len(conversions),

            "revenue": revenue,

            "product_scores": product_score
        }


    # =========================
    # OPTIMIZATION DECISION
    # =========================

    def optimize(self):

        analysis = self.analyze()


        if not analysis["best_product"]:

            return {
                "status": "no_data"
            }


        return {

            "status": "optimized",

            "action": "BOOST_PRODUCT",

            "product": analysis["best_product"],

            "revenue": analysis["revenue"]

        }
