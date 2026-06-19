from datetime import datetime


def run_orchestrator(products):
    try:
        if not products:
            return {
                "schedule": {},
                "status": "NO_PRODUCTS"
            }

        schedule = {
            "morning": [],
            "afternoon": [],
            "evening": []
        }

        for i, product in enumerate(products):
            product_id = product.get("product_id")

            if not product_id:
                continue

            if i % 3 == 0:
                slot = "morning"
            elif i % 3 == 1:
                slot = "afternoon"
            else:
                slot = "evening"

            schedule[slot].append({
                "product_id": product_id,
                "priority": product.get("score", 1)
            })

        return {
            "schedule": schedule,
            "generated_at": str(datetime.now()),
            "status": "ORCHESTRATOR_OK"
        }

    except Exception as e:
        return {
            "schedule": {},
            "error": str(e),
            "status": "ORCHESTRATOR_FAILED"
        }


class OrchestratorEngine:
    def __init__(self):
        print("🟢 OrchestratorEngine loaded")

    def build_tasks(self, products):
        return run_orchestrator(products)
