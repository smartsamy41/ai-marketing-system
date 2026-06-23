from datetime import datetime


# =========================
# BUILD SCHEDULE (SAFE)
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
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================
# LIVE AUTONOMY TRIGGER (SAFE + CI FRIENDLY)
# =========================
class SchedulerEngine:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def trigger_run(self):
        """
        SAFE MODE:
        - no hard dependency crash
        - optional import
        """

        try:
            import requests

            response = requests.get(
                f"{self.base_url}/run",
                timeout=10
            )

            return {
                "status": "SUCCESS",
                "response": response.json()
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }

    def create_schedule(self, products):
        return build_schedule(products)
