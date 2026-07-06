from datetime import datetime

class SheetsConnector:

    def __init__(self):

        # Local fallback memory (später echte Google Sheets API)
        self.db = {
            "clicks": [],
            "conversions": [],
            "events": [],
            "products": []
        }

    # =========================
    # CLICK TRACKING
    # =========================
    def log_click(self, product: str, source: str = "web"):

        self.db["clicks"].append({
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

        self.db["conversions"].append({
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
    # PRODUCT STORAGE
    # =========================
    def add_product(self, product: dict):

        self.db["products"].append({
            "data": product,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "status": "product_saved"
        }

    # =========================
    # EXPORT (FOR AI / ANALYTICS)
    # =========================
    def export(self):

        return self.db
