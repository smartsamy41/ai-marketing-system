class RevenueEngine:

    def __init__(self):

        self.clicks = 0
        self.conversions = 0
        self.revenue = 0.0

    def track_click(self):

        self.clicks += 1

    def track_conversion(self, value: float):

        self.conversions += 1
        self.revenue += value

    def stats(self):

        return {
            "clicks": self.clicks,
            "conversions": self.conversions,
            "revenue": self.revenue
        }
