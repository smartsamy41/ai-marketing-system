class MoneyTracking:

    def __init__(self):

        self.clicks = []
        self.conversions = []

    def log_click(self, product):

        self.clicks.append(product)

        return {"status": "click_saved"}

    def log_conversion(self, product, value):

        self.conversions.append({
            "product": product,
            "value": value
        })

        return {"status": "conversion_saved"}

    def revenue(self):

        return sum(c["value"] for c in self.conversions)
