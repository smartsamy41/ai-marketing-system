from engine.live_data_layer import LiveDataLayer


class ProductLayer:

    def __init__(self):

        self.live = LiveDataLayer()

    def get_all_products(self):

        return self.live.get_products()

    def get_by_partner(self, partner):

        return [
            p for p in self.get_all_products()
            if p.get("partner") == partner
        ]

    def load_product(self, product_id):

        return {
            "product_id": product_id,
            "status": "LIVE_LOADED"
        }
