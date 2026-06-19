from datetime import datetime


# =========================
# 🚀 ORCHESTRATOR ENGINE V2
# =========================

def run_orchestrator(products):

    try:

        print("🟢 OrchestratorEngine V2 running")

        if not products:
            return {"schedule": {}}

        schedule = {
            "morning": [],
            "afternoon": [],
            "evening": []
        }

        # =========================
        # SIMPLE INTELLIGENT DISTRIBUTION
        # =========================

        for i, product in enumerate(products):

            product_id = product.get("product_id")

            if not product_id:
                continue

            # rotation logic (simple load balancing)
            if i % 3 == 0:
                schedule["morning"].append({
                    "product_id": product_id,
                    "priority": product.get("score", 1)
                })

            elif i % 3 == 1:
                schedule["afternoon"].append({
                    "product_id": product_id,
                    "priority": product.get("score", 1)
                })

            else:
                schedule["evening"].append({
                    "product_id": product_id,
                    "priority": product.get("score", 1)
                })

        return {
            "schedule": schedule,
            "generated_at": str(datetime.now())
        }

    except Exception as e:

        return {
            "schedule": {},
            "error": str(e),
            "status": "orchestrator_failed"
        }
