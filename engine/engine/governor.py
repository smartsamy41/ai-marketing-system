from datetime import datetime


class Governor:

    def __init__(self):
        self.locks = {
            "landingpage": set(),
            "traffic": False,
            "autopilot": False
        }

    # =========================
    # LANDINGPAGE CHECK
    # =========================
    def can_create_landingpage(self, product_id):

        if product_id in self.locks["landingpage"]:
            return False

        self.locks["landingpage"].add(product_id)
        return True

    # =========================
    # TRAFFIC CONTROL
    # =========================
    def allow_traffic(self, amount):

        if amount > 10:
            return False
        return True

    # =========================
    # SYSTEM HEALTH GATE
    # =========================
    def system_ok(self, score):

        if score < 0.5:
            return False
        return True

    # =========================
    # MASTER DECISION
    # =========================
    def approve(self, product_id, traffic_amount, score):

        if not self.can_create_landingpage(product_id):
            return {"status": "BLOCKED", "reason": "LANDINGPAGE_EXISTS"}

        if not self.allow_traffic(traffic_amount):
            return {"status": "BLOCKED", "reason": "TRAFFIC_LIMIT"}

        if not self.system_ok(score):
            return {"status": "BLOCKED", "reason": "LOW_SCORE"}

        return {
            "status": "APPROVED",
            "timestamp": datetime.utcnow().isoformat()
        }
