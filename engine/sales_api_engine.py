import requests
from datetime import datetime

class SalesAPIEngine:

    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or "https://api.tarifcheck.example"
        self.api_key = api_key or "demo_key"
        self.logs = []

    # =========================
    # SEND LEAD (REAL CONNECTOR)
    # =========================
    def send_lead(self, product_id, source="api"):

        payload = {
            "product_id": product_id,
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }

        # REAL API CALL (SAFE FALLBACK)
        try:
            response = requests.post(
                f"{self.base_url}/lead",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=5
            )

            result = {
                "status": "SENT",
                "api_status": response.status_code,
                "product_id": product_id
            }

        except Exception as e:
            # fallback safe mode (NO CRASH)
            result = {
                "status": "FALLBACK_LOG_ONLY",
                "error": str(e),
                "product_id": product_id
            }

        self.logs.append(result)
        return result

    # =========================
    # STATS
    # =========================
    def get_sales_stats(self):

        return {
            "total_leads": len(self.logs),
            "last_status": self.logs[-1] if self.logs else None
        }
