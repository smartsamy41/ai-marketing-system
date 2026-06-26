class ProductLayer:

    def __init__(self):
        pass

    def get_all_products(self):
        return [
            {"product_id": "CHK24_001", "partner": "check24"},
            {"product_id": "TC_001", "partner": "tarifcheck"},
            {"product_id": "AMZ_001", "partner": "amazon"}
        ]

    def get_by_partner(self, partner):
        return [
            p for p in self.get_all_products()
            if p.get("partner") == partner
        ]

    def load_product(self, product_id):
        return {
            "product_id": product_id,
            "status": "SAFE_LOADED"
        }
