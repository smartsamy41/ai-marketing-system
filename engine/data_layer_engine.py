from datetime import datetime


# =========================
# SIMPLE DATA STORAGE LAYER
# =========================
class DataLayer:

    def __init__(self):

        self.leads = []
        self.sales = []
        self.events = []

    # =========================
    # STORE EMAIL LEAD
    # =========================
    def save_lead(self, email, source="landingpage"):

        lead = {
            "email": email,
            "source": source,
            "status": "PENDING_DOI",
            "created_at": datetime.utcnow().isoformat()
        }

        self.leads.append(lead)

        return lead

    # =========================
    # STORE SALE EVENT
    # =========================
    def save_sale(self, product, amount, status="open"):

        sale = {
            "product": product,
            "amount": amount,
            "status": status,
            "created_at": datetime.utcnow().isoformat()
        }

        self.sales.append(sale)

        return sale

    # =========================
    # TRACK EVENT
    # =========================
    def track_event(self, event_type, data):

        event = {
            "type": event_type,
            "data": data,
            "time": datetime.utcnow().isoformat()
        }

        self.events.append(event)

        return event

    # =========================
    # DASHBOARD DATA
    # =========================
    def get_dashboard(self):

        return {
            "leads": len(self.leads),
            "sales": len(self.sales),
            "events": len(self.events)
        }
