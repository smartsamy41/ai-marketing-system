class OrchestratorEngine:

    def __init__(self):
        print("🟢 OrchestratorEngine loaded")

    def build_tasks(self, products):

        if not products:
            return {"schedule": {}}

        schedule = {
            "morning": [],
            "afternoon": [],
            "evening": []
        }

        for i, product in enumerate(products):

            target = list(schedule.keys())[i % 3]

            schedule[target].append({
                "product_id": product.get("product_id"),
                "score": product.get("score", 1)
            })

        return {"schedule": schedule}
