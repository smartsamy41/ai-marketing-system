from datetime import datetime

class V9RealWorldEngine:

    def __init__(self, conversion_engine):

        self.conversion = conversion_engine
        self.sales_events = []
        self.real_revenue = 0.0

    # =========================
    # REAL SALES API CONNECT (TARIFCHECK / CHECK24 / AMAZON)
    # =========================
    def send_to_sales_api(self, product_id, source="landingpage"):

        # SIMULATION SAFE PLACEHOLDER (later real API)
        event = {
            "product_id": product_id,
            "source": source,
            "status": "SENT_TO_SALES_API",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.sales_events.append(event)

        return event

    # =========================
    # CONVERSION CONFIRMATION (REAL MONEY EVENT)
    # =========================
    def confirm_conversion(self, product_id, revenue):

        self.real_revenue += revenue

        conversion = {
            "product_id": product_id,
            "revenue": revenue,
            "status": "CONFIRMED_REAL_REVENUE",
            "timestamp": datetime.utcnow().isoformat()
        }

        return conversion

    # =========================
    # REAL WORLD SCORE
    # =========================
    def score(self):

        clicks = len(self.conversion.clicks)
        conversions = len(self.conversion.conversions)

        return {
            "clicks": clicks,
            "conversions": conversions,
            "real_revenue": self.real_revenue,
            "revenue_per_click": self.real_revenue / clicks if clicks else 0
        }

    # =========================
    # SYSTEM REPORT
    # =========================
    def report(self):

        return {
            "sales_events": len(self.sales_events),
            "real_revenue": self.real_revenue,
            "timestamp": datetime.utcnow().isoformat()
        }
