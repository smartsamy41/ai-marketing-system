from datetime import datetime
import random


class TrafficEngine:

    def __init__(self):
        self.visits = []
        self.sources = [
            "pinterest",
            "youtube",
            "google_seo",
            "blog",
            "direct"
        ]

    # =========================
    # REALISTIC TRAFFIC GENERATION
    # =========================
    def generate_visit(self, product_id, source=None):

        if source is None:
            source = random.choice(self.sources)

        visit = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "clicked": True
        }

        self.visits.append(visit)

        return {
            "status": "VISIT_CREATED",
            "visit": visit
        }

    # =========================
    # BULK TRAFFIC (CAMPAIGN MODE)
    # =========================
    def run_bulk_traffic(self, products):

        results = []

        for p in products:
            # weighted traffic simulation (realistic funnel behavior)
            visits_per_product = random.randint(3, 8)

            for _ in range(visits_per_product):
                results.append(self.generate_visit(p))

        return {
            "status": "TRAFFIC_CAMPAIGN_DONE",
            "total_visits": len(results),
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # STATS
    # =========================
    def get_stats(self):

        total = len(self.visits)

        source_stats = {}
        for v in self.visits:
            s = v["source"]
            source_stats[s] = source_stats.get(s, 0) + 1

        return {
            "total_visits": total,
            "sources": source_stats,
            "timestamp": datetime.utcnow().isoformat()
        }
