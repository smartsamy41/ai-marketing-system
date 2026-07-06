from datetime import datetime

class SheetsEngine:

    def __init__(self):
        self.data = {
            "clicks": [],
            "conversions": [],
            "products": [],
            "pages": []
        }

    # =========================
    # CLICK TRACKING
    # =========================
    def log_click(self, product: str, source: str = "direct"):

        self.data["clicks"].append({
            "product": product,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "status": "click_logged",
            "product": product
        }

    # =========================
    # CONVERSION TRACKING
    # =========================
    def log_conversion(self, product: str, value: float):

        self.data["conversions"].append({
            "product": product,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "status": "conversion_logged",
            "product": product,
            "value": value
        }

    # =========================
    # DATA EXPORT (FOR AI LATER)
    # =========================
    def export_data(self):

        return self.data
