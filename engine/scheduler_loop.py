import time

class SchedulerLoop:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator
        self.running = True

    # =========================
    # MAIN LOOP (24/7 AI ENGINE)
    # =========================
    def start(self, interval_seconds: int = 300):

        while self.running:

            try:

                result = self.orchestrator.run()

                print("🚀 AUTOPILOT CYCLE:", result)

            except Exception as e:

                print("⚠️ ERROR:", str(e))

            time.sleep(interval_seconds)

    # =========================
    # STOP ENGINE
    # =========================
    def stop(self):

        self.running = False
