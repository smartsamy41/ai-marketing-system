from datetime import datetime


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


class SchedulerEngine:

    def __init__(self):
        print("🟢 SchedulerEngine loaded")

    def create_schedule(self, products):
        return build_schedule(products)
