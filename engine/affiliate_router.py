from datetime import datetime


class AffiliateRouter:

    def __init__(self):
        self.routes = {
            "CHK24_001": "https://check24.example/strom",
            "TC_001": "https://tarifcheck.example/solar",
            "AMZ_001": "https://amazon.example/product"
        }

    def get_redirect(self, product_id):

        return {
            "product_id": product_id,
            "url": self.routes.get(product_id, "https://default-link.com"),
            "timestamp": datetime.utcnow().isoformat()
        }
