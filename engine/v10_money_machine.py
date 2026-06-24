from datetime import datetime

class V10MoneyMachine:

    def __init__(self, v9_engine, conversion_engine):

        self.v9 = v9_engine
        self.conversion = conversion_engine

        self.big_memory = []
        self.revenue_stream = 0.0

    # =========================
    # INGEST REAL DATA
    # =========================
    def ingest(self, product_id, revenue=0.0, source="sales_api"):

        event = {
            "product_id": product_id,
            "revenue": revenue,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.big_memory.append(event)
        self.revenue_stream += revenue

        return {"status": "INGESTED", "event": event}

    # =========================
    # ANALYTICS CORE
    # =========================
    def analyze(self):

        if not self.big_memory:
            return {"status": "NO_DATA"}

        clicks = len(self.conversion.clicks)
        conversions = len(self.conversion.conversions)

        avg_revenue = self.revenue_stream / conversions if conversions else 0

        score = (clicks * 0.1) + (conversions * 5) + (avg_revenue * 2)

        if score > 100:
            decision = "HYPER_SCALE"
        elif score > 50:
            decision = "SCALE"
        elif score > 20:
            decision = "OPTIMIZE"
        else:
            decision = "RESTRUCTURE"

        return {
            "score": round(score, 2),
            "decision": decision,
            "revenue": self.revenue_stream,
            "clicks": clicks,
            "conversions": conversions,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # AUTO ALLOCATION ENGINE
    # =========================
    def allocate(self):

        analysis = self.analyze()

        if analysis["decision"] == "HYPER_SCALE":
            action = "INCREASE_ALL_CHANNELS"
        elif analysis["decision"] == "SCALE":
            action = "BOOST_WINNERS"
        elif analysis["decision"] == "OPTIMIZE":
            action = "CUT_LOW_PERFORMERS"
        else:
            action = "REBUILD_FUNNEL"

        return {
            "action": action,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # FULL MONEY LOOP
    # =========================
    def run_cycle(self, product_id):

        self.ingest(product_id, revenue=10.0, source="simulation")

        return {
            "status": "V10_CYCLE_DONE",
            "analysis": self.analyze(),
            "allocation": self.allocate()
        }

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total_events": len(self.big_memory),
            "total_revenue": self.revenue_stream,
            "timestamp": datetime.utcnow().isoformat()
        }
