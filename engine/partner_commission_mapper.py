class PartnerCommissionMapper:

    def __init__(self):

        # =========================
        # FIXED COMMISSION TABLE
        # =========================
        self.commissions = {
            "CHK24_001": 25.0,
            "TC_001": 30.0,
            "AMZ_001": 8.0
        }

    # =========================
    # GET COMMISSION
    # =========================
    def get(self, product_id):

        value = self.commissions.get(product_id, 0.0)

        return {
            "product_id": product_id,
            "commission_eur": value,
            "currency": "EUR"
        }

    # =========================
    # CALCULATE REVENUE
    # =========================
    def calculate(self, product_id, leads=1):

        value = self.commissions.get(product_id, 0.0)

        revenue = value * leads

        return {
            "product_id": product_id,
            "leads": leads,
            "commission_per_lead": value,
            "revenue_total": revenue
        }
