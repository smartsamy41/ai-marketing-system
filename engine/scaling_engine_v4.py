from datetime import datetime

class ScalingEngineV4:

    def __init__(self, conversion_engine):

        self.conversion_engine = conversion_engine
        self.history = []

    # =========================
    # ANALYZE ALL PRODUCTS
    # =========================
    def analyze_product(self, product_id):

        score_data = self.conversion_engine.product_score(product_id)

        score = score_data["score"]
        revenue = score_data["revenue"]
        clicks = score_data["clicks"]
        conversions = score_data["conversions"]

        # =========================
        # SCALING LOGIC
        # =========================
        if score >= 50 and revenue > 20:
            decision = "SCALE"
        elif score >= 20:
            decision = "BOOST"
        else:
            decision = "STOP"

        result = {
            "product_id": product_id,
            "decision": decision,
            "score": score,
            "revenue": revenue,
            "clicks": clicks,
            "conversions": conversions,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.history.append(result)

        return result

    # =========================
    # BATCH SCAN (FULL SYSTEM OPTIMIZATION)
    # =========================
    def scan_all(self, product_list):

        results = []

        for p in product_list:
            results.append(self.analyze_product(p))

        return {
            "status": "SCANNED",
            "results": results
        }

    # =========================
    # SYSTEM REPORT
    # =========================
    def report(self):

        scale = len([h for h in self.history if h["decision"] == "SCALE"])
        boost = len([h for h in self.history if h["decision"] == "BOOST"])
        stop = len([h for h in self.history if h["decision"] == "STOP"])

        return {
            "scale": scale,
            "boost": boost,
            "stop": stop,
            "total": len(self.history)
        }
