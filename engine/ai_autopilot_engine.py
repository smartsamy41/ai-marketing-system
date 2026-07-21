class AutopilotEngine:

    def __init__(self, ai_core, content_ai, affiliate=None):
        self.ai = ai_core
        self.content = content_ai
        self.affiliate = affiliate

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
        content_input = product

        if self.affiliate:
            product_data = self.affiliate.get_product_data(
                product
            )

            if product_data.get("status") == "FOUND":
                content_input = product_data

        content = self.content.generate(
            content_input
        )

        # 5. FINAL OUTPUT (CLEAN PIPELINE)
        return {
            "status": "READY_TO_PUBLISH",
            "product": product,
            "title": content.get("title"),
            "description": content.get("description"),
            "reason": decision.get("reason", "ai_selected_best_product")
        }
