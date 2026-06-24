from datetime import datetime

class ConversionTrackingV3:

    def __init__(self):
        self.clicks = []
        self.leads = []
        self.conversions = []
        self.revenue_log = []

    # =========================
    # CLICK TRACK
    # =========================
    def track_click(self, product_id, source="api"):

        click = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.clicks.append(click)

        return {"status": "CLICK_TRACKED", "click": click}

    # =========================
    # LEAD (SALES API)
    # =========================
    def track_lead(self, product_id, source="sales_api"):

        lead = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.leads.append(lead)

        return {"status": "LEAD_TRACKED", "lead": lead}

    # =========================
    # CONVERSION (REAL MONEY EVENT)
    # =========================
    def track_conversion(self, product_id, revenue=0.0):

        conversion = {
            "product_id": product_id,
            "revenue": revenue,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.conversions.append(conversion)
        self.revenue_log.append(revenue)

        return {"status": "CONVERSION_TRACKED", "conversion": conversion}

    # =========================
    # PRODUCT SCORE (AI SCALING INPUT)
    # =========================
    def product_score(self, product_id):

        clicks = len([c for c in self.clicks if c["product_id"] == product_id])
        leads = len([l for l in self.leads if l["product_id"] == product_id])
        conversions = len([c for c in self.conversions if c["product_id"] == product_id])
        revenue = sum(self.revenue_log)

        score = (clicks * 0.1) + (leads * 2) + (conversions * 10) + (revenue * 0.05)

        return {
            "product_id": product_id,
            "score": round(score, 2),
            "clicks": clicks,
            "leads": leads,
            "conversions": conversions,
            "revenue": revenue
        }

    # =========================
    # SYSTEM REPORT
    # =========================
    def report(self):

        return {
            "clicks": len(self.clicks),
            "leads": len(self.leads),
            "conversions": len(self.conversions),
            "total_revenue": sum(self.revenue_log)
        }
