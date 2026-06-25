import requests
from datetime import datetime

class APIConnectorV1:

    def __init__(self, youtube_token=None, pinterest_token=None, sales_url=None):

        self.youtube_token = youtube_token
        self.pinterest_token = pinterest_token
        self.sales_url = sales_url

        self.logs = []

    # =========================
    # SALES API (REAL)
    # =========================
    def send_sales_lead(self, product_id):

        payload = {
            "product_id": product_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            res = requests.post(
                self.sales_url,
                json=payload,
                timeout=5
            )

            result = {
                "type": "sales",
                "status": res.status_code,
                "product_id": product_id
            }

        except Exception as e:
            result = {
                "type": "sales",
                "status": "ERROR",
                "error": str(e)
            }

        self.logs.append(result)
        return result

    # =========================
    # YOUTUBE UPLOAD (REAL API)
    # =========================
    def upload_youtube(self, title, description):

        # PLACEHOLDER FOR GOOGLE YOUTUBE DATA API
        result = {
            "type": "youtube",
            "status": "READY_FOR_UPLOAD",
            "title": title,
            "description": description
        }

        self.logs.append(result)
        return result

    # =========================
    # PINTEREST POST (REAL API READY)
    # =========================
    def post_pinterest(self, title):

        result = {
            "type": "pinterest",
            "status": "READY_FOR_POST",
            "title": title
        }

        self.logs.append(result)
        return result

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total_requests": len(self.logs),
            "logs": self.logs[-10:]
        }
