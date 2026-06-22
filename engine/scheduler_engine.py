from datetime import datetime

import requests


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
# LIVE AUTONOMY TRIGGER
# =========================
class SchedulerEngine:

    def __init__(self, base_url):
        self.base_url = base_url
        print("🟢 SchedulerEngine ACTIVE")

    def trigger_run(self):
        try:
            response = requests.get(self.base_url + "/run")

            print("🟢 AUTONOMY TRIGGERED")
            print("STATUS:", response.status_code)

            return response.json()

        except Exception as e:
            print("❌ ERROR TRIGGERING SYSTEM:", str(e))
            return {"status": "ERROR", "message": str(e)}

    def create_schedule(self, products):
        return build_schedule(products)
