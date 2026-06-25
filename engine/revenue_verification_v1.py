from datetime import datetime

class RevenueVerificationV1:

    def __init__(self):
        self.leads = []

    # =========================
    # SEND LEAD (TRACKED)
    # =========================
    def send_lead(self, product_id, source="api"):

        lead = {
            "product_id": product_id,
            "source": source,
            "status": "SENT",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.leads.append(lead)

        return lead

    # =========================
    # UPDATE STATUS (REAL FEEDBACK)
    # =========================
    def update_status(self, product_id, status):

        for lead in self.leads:
            if lead["product_id"] == product_id:
                lead["status"] = status
                lead["updated_at"] = datetime.utcnow().isoformat()

                return lead

        return {"status": "NOT_FOUND"}

    # =========================
    # REVENUE ANALYTICS
    # =========================
    def report(self):

        summary = {
            "sent": 0,
            "confirmed": 0,
            "failed": 0,
            "unknown": 0
        }

        for lead in self.leads:
            s = lead["status"]
            if s == "SENT":
                summary["sent"] += 1
            elif s == "CONFIRMED":
                summary["confirmed"] += 1
            elif s == "FAILED":
                summary["failed"] += 1
            else:
                summary["unknown"] += 1

        return {
            "summary": summary,
            "total_leads": len(self.leads)
        }
