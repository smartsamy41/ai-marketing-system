from datetime import datetime


class MonetizationControlLayer:

    def __init__(self):

        self.clicks = []
        self.revenue_events = []
        self.conversions = []

        # =========================
        # LIVE MODE SAFETY
        # =========================
        self.LIVE_MODE = False

    # =========================
    # CLICK TRACKING
    # =========================
    def track_click(self, product_id, source="unknown"):

        event = {
            "type": "click",
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.clicks.append(event)

        return event

    # =========================
    # CONVERSION TRACKING
    # =========================
    def track_conversion(self, product_id, value=0.0):

        event = {
            "type": "conversion",
            "product_id": product_id,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.conversions.append(event)

        return event

    # =========================
    # REVENUE TRACKING
    # =========================
    def track_revenue(self, product_id, amount):

        event = {
            "type": "revenue",
            "product_id": product_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.revenue_events.append(event)

        return event

    # =========================
    # PERFORMANCE REPORT
    # =========================
    def get_report(self):

        return {
            "clicks": len(self.clicks),
            "conversions": len(self.conversions),
            "revenue_events": len(self.revenue_events),
            "total_revenue": sum([r["amount"] for r in self.revenue_events]) if self.revenue_events else 0,
            "status": "MONETIZATION_CONTROL_ACTIVE"
        }

    # =========================
    # SAFE LIVE HOOK (NO REAL PUBLISH YET)
    # =========================
    def safe_live_trigger(self, product_id):

        if not self.LIVE_MODE:

            return {
                "status": "SAFE_MODE",
                "action": "NO_REAL_MONETIZATION"
            }

        return {
            "status": "LIVE_MONETIZATION_ACTIVE",
            "product_id": product_id
        }
