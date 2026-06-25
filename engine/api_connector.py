from datetime import datetime

class APIConnector:

    def __init__(self):
        self.logs = []

    # =========================
    # SALES (MOCK SAFE)
    # =========================
    def send_sales_lead(self, product_id, source="api"):

        log = {
            "type": "sales",
            "product_id": product_id,
            "status": "MOCK_SENT",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)
        return log

    # =========================
    # YOUTUBE (MOCK SAFE)
    # =========================
    def upload_youtube_video(self, title, description):

        log = {
            "type": "youtube",
            "title": title,
            "status": "MOCK_READY",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)
        return log

    # =========================
    # PINTEREST (MOCK SAFE)
    # =========================
    def create_pinterest_pin(self, title):

        log = {
            "type": "pinterest",
            "title": title,
            "status": "MOCK_READY",
            "timestamp": datetime.utcnow().isoformat()
        }

        self.logs.append(log)
        return log

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "total": len(self.logs),
            "logs": self.logs[-10:]
        }
