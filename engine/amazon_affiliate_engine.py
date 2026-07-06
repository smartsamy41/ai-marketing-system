class AmazonAffiliateEngine:
    def __init__(self):
        self.products = {
            "AMZ_001": {
                "title": "Produkt 1",
                "url": "https://amazon.de/dp/XXXX?tag=freebasics-21"
            },
            "AMZ_002": {
                "title": "Produkt 2",
                "url": "https://amazon.de/dp/YYYY?tag=freebasics-21"
            }
        }

        self.click_log = []
        self.conversion_log = []

    def get_link(self, product_id: str):
        product = self.products.get(product_id)
        if not product:
            return None
        return product["url"]

    def track_click(self, product_id: str):
        self.click_log.append(product_id)
        return {"status": "click_tracked", "product_id": product_id}

    def track_conversion(self, product_id: str, amount: float):
        self.conversion_log.append({
            "product_id": product_id,
            "amount": amount
        })
        return {"status": "conversion_tracked"}

    def stats(self):
        total = sum(x["amount"] for x in self.conversion_log)
        return {
            "clicks": len(self.click_log),
            "conversions": len(self.conversion_log),
            "revenue": total
        }
