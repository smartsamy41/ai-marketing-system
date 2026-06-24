from datetime import datetime
import random


# =========================
# TRAFFIC ENGINE (SIMULATION + READY FOR REAL SOURCES)
# =========================
class TrafficEngine:

    def __init__(self):

        self.sources = [
            "pinterest",
            "youtube",
            "seo",
            "blog",
            "direct"
        ]

        self.visits = []

    # =========================
    # GENERATE TRAFFIC EVENT
    # =========================
    def generate_traffic(self, product_id):

        source = random.choice(self.sources)

        visit = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "converted": random.random() < 0.05  # 5% conversion sim
        }

        self.visits.append(visit)

        return {
            "status": "TRAFFIC_GENERATED",
            "visit": visit
        }

    # =========================
    # BULK TRAFFIC SIMULATION
    # =========================
    def run_bulk_traffic(self, products):

        results = []

        for p in products:

            results.append(self.generate_traffic(p))

        return {
            "status": "BULK_TRAFFIC_DONE",
            "total": len(results),
            "results": results
        }

    # =========================
    # ANALYTICS
    # =========================
    def get_stats(self):

        total = len(self.visits)
        conversions = len([v for v in self.visits if v["converted"]])
        sources = {}

        for v in self.visits:
            s = v["source"]
            sources[s] = sources.get(s, 0) + 1

        return {
            "total_visits": total,
            "conversions": conversions,
            "conversion_rate": round(conversions / total, 4) if total > 0 else 0,
            "sources": sources
        }
