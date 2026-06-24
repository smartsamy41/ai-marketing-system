from datetime import datetime


class Governor:

    def __init__(self):
        self.landingpage_lock = set()

    # =========================
    # LANDINGPAGE CHECK
    # =========================
    def can_create_landingpage(self, product_id):

        if product_id in self.landingpage_lock:
            return False

        self.landingpage_lock.add(product_id)
        return True

    # =========================
    # TRAFFIC CHECK
    # =========================
    def allow_traffic(self, traffic_amount):

        return traffic_amount <= 10

    # =========================
    # SCORE CHECK
    # =========================
    def system_ok(self, score):

        return score >= 0.5

    # =========================
    # MASTER APPROVAL
    # =========================
    def approve(self, product_id, traffic_amount, score):

        if not self.can_create_landingpage(product_id):
            return {
                "status": "BLOCKED",
                "reason": "LANDINGPAGE_EXISTS"
            }

        if not self.allow_traffic(traffic_amount):
            return {
                "status": "BLOCKED",
                "reason": "TRAFFIC_LIMIT"
            }

        if not self.system_ok(score):
            return {
                "status": "BLOCKED",
                "reason": "LOW_SCORE"
            }

        return {
            "status": "APPROVED",
            "timestamp": datetime.utcnow().isoformat()
        }
