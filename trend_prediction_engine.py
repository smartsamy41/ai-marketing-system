from datetime import datetime


class TrendPredictionEngine:

    def __init__(self):

        # =========================
        # BASE SIGNALS
        # =========================
        self.signals = [
            "strom preis steigt",
            "gas energie krise",
            "inflation kredit nachfrage",
            "versicherung kosten 2026",
            "amazon deals trend",
            "dsl glasfaser ausbau",
            "e autos versicherung",
            "zinsen steigen europa"
        ]

        self.trends = []

    # =========================
    # SIGNAL EXPANSION
    # =========================
    def expand_signal(self, signal):

        return [
            f"{signal} 2026",
            f"beste {signal}",
            f"{signal} prognose",
            f"{signal} vergleich",
            f"{signal} auswirkungen",
            f"{signal} steigende nachfrage"
        ]

    # =========================
    # TREND DETECTION ENGINE
    # =========================
    def detect_trends(self):

        detected = []

        for signal in self.signals:

            expanded = self.expand_signal(signal)

            for item in expanded:

                score = len(item) % 10 + 1  # pseudo trend score

                detected.append({
                    "trend": item,
                    "base_signal": signal,
                    "score": score,
                    "status": "TREND_DETECTED"
                })

        self.trends = detected

        return {
            "status": "TRENDS_DETECTED",
            "count": len(detected),
            "trends": detected,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # PRIORITY TREND FILTER
    # =========================
    def top_trends(self, limit=10):

        sorted_trends = sorted(
            self.trends,
            key=lambda x: x["score"],
            reverse=True
        )

        return {
            "status": "TOP_TRENDS_READY",
            "top": sorted_trends[:limit]
        }

    # =========================
    # TREND → PRODUCT GENERATION
    # =========================
    def to_products(self):

        products = []

        for i, t in enumerate(self.trends):

            products.append({
                "product_id": f"TREND_{i:04d}",
                "title": f"{t['trend']} Vergleich 2026",
                "keyword": t["trend"],
                "score": t["score"],
                "category": "trend_based",
                "status": "AUTO_TREND_PRODUCT"
            })

        return {
            "status": "TREND_PRODUCTS_CREATED",
            "count": len(products),
            "products": products
        }
