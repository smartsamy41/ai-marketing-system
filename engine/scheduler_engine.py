from datetime import datetime


# =========================
# BUILD SCHEDULE
# =========================
def build_schedule(products):

    schedule = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }

    for i, product in enumerate(products):

        if i % 3 == 0:
            schedule["morning"].append(product)
        elif i % 3 == 1:
            schedule["afternoon"].append(product)
        else:
            schedule["evening"].append(product)

    return {
        "status": "SCHEDULE_CREATED",
        "schedule": schedule,
        "timestamp": str(datetime.now())
    }


# =========================
# LIVE AUTONOMY TRIGGER (SAFE)
# =========================
class SchedulerEngine:

    def __init__(self, base_url):
        self.base_url = base_url

    def trigger_run(self):
        import requests   # 🔥 IMPORTANT: local import (safe)

        try:
            response = requests.get(self.base_url + "/run")
            return response.json()

        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def create_schedule(self, products):
        return build_schedule(products)
