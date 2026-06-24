import requests
from datetime import datetime

class SalesAPIEngine:

    def __init__(self):
        self.conversions = []

        # Tarifcheck Config (Placeholder – später echte API Keys)
        self.api_url = "https://api.tarifcheck.de/sales"
        self.partner_id = "165274"

    # =========================
    # SEND CLICK / LEAD
    # =========================
    def send_lead(self, product_id, source="autopilot"):

        payload = {
            "partner_id": self.partner_id,
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            # REAL API CALL (wenn aktiv)
            # response = requests.post(self.api_url, json=payload)

            # SAFE SIMULATION MODE (bis API aktiv)
            response = {"status": "SIMULATED_LEAD_SENT"}

        except Exception as e:
            response = {"status": "ERROR", "message": str(e)}

        self.conversions.append(payload)

        return {
            "status": "LEAD_PROCESSED",
            "api_response": response,
            "payload": payload
        }

    # =========================
    # STATS
    # =========================
    def get_sales_stats(self):

        return {
            "total_leads": len(self.conversions),
            "status": "ACTIVE"
        }
