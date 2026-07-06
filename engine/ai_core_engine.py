class AICoreEngine:

    def __init__(self, sheets_api):
        self.sheets = sheets_api

    # =========================
    # FULL ANALYSIS LOOP
    # =========================
    def run_analysis(self):

        data = self.sheets.export()

        clicks = data["clicks"]
        conversions = data["conversions"]

        score = {}

        # -------------------------
        # CLICK INTELLIGENCE
        # -------------------------
        for c in clicks:
            p = c["product"]
            score[p] = score.get(p, 0) + 1

        # -------------------------
        # REVENUE INTELLIGENCE
        # -------------------------
        revenue = 0

        for c in conversions:
            revenue += c["value"]

        # -------------------------
        # TOP PRODUCT DETECTION
        # -------------------------
        top = sorted(score.items(), key=lambda x: x[1], reverse=True)

        return {
            "clicks": len(clicks),
            "conversions": len(conversions),
            "revenue": revenue,
            "top_products": top
        }

    # =========================
    # AUTO DECISION ENGINE
    # =========================
    def decide_next_action(self):

        analysis = self.run_analysis()

        if analysis["clicks"] < 3:
            return {
                "action": "WAIT",
                "reason": "not enough data"
            }

        if not analysis["top_products"]:
            return {
                "action": "WAIT",
                "reason": "no products yet"
            }

        best = analysis["top_products"][0][0]

        return {
            "action": "PUBLISH",
            "product": best,
            "reason": "highest performance detected"
        }
