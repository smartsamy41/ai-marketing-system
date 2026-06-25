from datetime import datetime

class RevenueVerificationV2:

    def __init__(self):
        self.leads = []

    # =========================
    # STEP 1: SEND LEAD
    # =========================
    def send_lead(self, product_id, source="api"):

        lead = {
            "product_id": product_id,
            "source": source,
            "status": "SENT",
            "revenue": 0,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.leads.append(lead)

        return lead

    # =========================
    # STEP 2: UPDATE FROM SALES API
    # =========================
    def update_from_sales(self, product_id, status, revenue=0):

        for lead in self.leads:
            if lead["product_id"] == product_id:

                lead["status"] = status  # CONFIRMED / REJECTED
                lead["revenue"] = revenue
                lead["updated_at"] = datetime.utcnow().isoformat()

                return lead

        return {"status": "NOT_FOUND"}

    # =========================
    # STEP 3: REVENUE ANALYTICS
    # =========================
    def analytics(self):

        total = len(self.leads)
        confirmed = len([l for l in self.leads if l["status"] == "CONFIRMED"])
        rejected = len([l for l in self.leads if l["status"] == "REJECTED"])
        revenue = sum([l["revenue"] for l in self.leads])

        return {
            "total_leads": total,
            "confirmed": confirmed,
            "rejected": rejected,
            "revenue": revenue,
            "conversion_rate": (confirmed / total) if total > 0 else 0
        }

    # =========================
    # STEP 4: LEARNING SIGNAL
    # =========================
    def best_products(self):

        scores = {}

        for l in self.leads:
            pid = l["product_id"]

            if pid not in scores:
                scores[pid] = {"revenue": 0, "count": 0}

            scores[pid]["revenue"] += l["revenue"]
            scores[pid]["count"] += 1

        return scores
