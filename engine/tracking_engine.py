from datetime import datetime


class TrackingEngine:

    def __init__(self):
        self.clicks = []
        self.conversions = []

    # =========================
    # TRACK CLICK
    # =========================
    def track_click(self, product_id, source="api"):

        click = {
            "product_id": product_id,
            "source": source,
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
    def track_conversion(self, product_id, value=0):

        conversion = {
            "product_id": product_id,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.conversions.append(conversion)

        return {
            "status": "CONVERSION_TRACKED",
            "conversion": conversion
        }

    # =========================
    # SUMMARY
    # =========================
    def get_summary(self):

        return {
            "clicks": len(self.clicks),
            "conversions": len(self.conversions)
        }
