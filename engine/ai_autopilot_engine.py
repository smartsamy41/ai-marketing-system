class AutopilotEngine:

    def __init__(self, ai_core, content_ai):
        self.ai = ai_core
        self.content = content_ai

    # =========================
    # MAIN AUTOPILOT LOOP
    # =========================
    def run(self):

        # 1. AI DECISION
        decision = self.ai.decide_next_action()

        # 2. SAFETY CHECK: WAIT STATE
        if decision["action"] == "WAIT":
            return {
                "status": "WAIT",
                "reason": decision.get("reason", "no reason provided")
            }

        # 3. PRODUCT SELECTION
        product = decision.get("product")

        if not product:
            return {
                "status": "ERROR",
                "reason": "no product returned by AI decision engine"
            }

        # 4. CONTENT GENERATION
        content = self.content.generate(product)

        # 5. FINAL OUTPUT (CLEAN PIPELINE)
        return {
            "status": "READY_TO_PUBLISH",
            "product": product,
            "title": content.get("title"),
            "description": content.get("description"),
            "reason": decision.get("reason", "ai_selected_best_product")
        }
