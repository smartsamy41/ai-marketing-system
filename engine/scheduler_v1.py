from datetime import datetime

class SchedulerV1:

    def __init__(self, content_engine):

        self.content = content_engine
        self.queue = []
        self.log = []

    # =========================
    # DEFINE DAILY SLOTS
    # =========================
    def get_slot(self):

        hour = datetime.utcnow().hour

        if 6 <= hour < 12:
            return "MORNING"
        elif 12 <= hour < 18:
            return "MIDDAY"
        else:
            return "EVENING"

    # =========================
    # PROCESS LIMITED BATCH
    # =========================
    def run(self, products):

        slot = self.get_slot()

        # LIMIT SYSTEM (ANTI-SPAM)
        limited = products[:3]

        results = []

        for p in limited:

            result = self.content.generate(p)

            results.append({
                "slot": slot,
                "product": p,
                "result": result
            })

        event = {
            "slot": slot,
            "count": len(results),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.log.append(event)

        return {
            "status": "SCHEDULER_V1_DONE",
            "slot": slot,
            "results": results
        }

    # =========================
    # REPORT
    # =========================
    def report(self):

        return {
            "runs": len(self.log),
            "last": self.log[-1] if self.log else None
        }
