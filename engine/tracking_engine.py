from datetime import datetime
import uuid


# =========================
# CLICK + REVENUE TRACKING ENGINE
# =========================
class TrackingEngine:

    def __init__(self):

        self.clicks = []
        self.conversions = []
        self.revenue = []

    # =========================
    # TRACK CLICK
    # =========================
    def track_click(self, product_id, source, link_type="affiliate"):

        click = {
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "source": source,
            "link_type": link_type,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.clicks.append(click)

        return {
            "status": "CLICK_TRACKED",
            "click": click
        }

    # =========================
    # TRACK CONVERSION
    # =========================
    def track_conversion(self, product_id, amount, provider):

        conversion = {
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "amount": amount,
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.conversions.append(conversion)

        return {
            "status": "CONVERSION_TRACKED",
            "conversion": conversion
        }

    # =========================
    # ADD REVENUE ENTRY
    # =========================
    def add_revenue(self, product_id, amount):

        entry = {
            "id": str(uuid.uuid4()),
            "product_id": product_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.revenue.append(entry)

        return {
            "status": "REVENUE_ADDED",
            "entry": entry
        }

    # =========================
    # DASHBOARD SUMMARY
    # =========================
    def get_summary(self):

        total_clicks = len(self.clicks)
        total_conversions = len(self.conversions)
        total_revenue = sum([r["amount"] for r in self.revenue]) if self.revenue else 0

        return {
            "clicks": total_clicks,
            "conversions": total_conversions,
            "revenue": total_revenue
        }
