from datetime import datetime
import requests


# =========================
# AUTOPILOT SCHEDULER ENGINE
# =========================
class SchedulerEngine:

    def __init__(self, base_url):
        self.base_url = base_url

    # =========================
    # RUN SYSTEM (TRIGGER /run)
    # =========================
    def trigger_run(self):

        try:
            response = requests.get(self.base_url + "/run")

            return {
                "status": "TRIGGERED",
                "code": response.status_code,
                "result": response.json()
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e)
            }

    # =========================
    # RUN CAMPAIGN (EMAIL AUTOPILOT)
    # =========================
    def trigger_campaign(self):

        try:
            response = requests.get(self.base_url + "/campaign")

            return {
                "status": "CAMPAIGN_TRIGGERED",
                "code": response.status_code,
                "result": response.json()
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e)
            }

    # =========================
    # FULL AUTOPILOT LOOP
    # =========================
    def autopilot_cycle(self):

        run_result = self.trigger_run()
        campaign_result = self.trigger_campaign()

        return {
            "status": "AUTOPILOT_CYCLE_DONE",
            "run": run_result,
            "campaign": campaign_result,
            "timestamp": str(datetime.utcnow())
        }
