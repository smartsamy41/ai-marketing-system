class AutopilotEngine:

    def __init__(self, ai_core, content_ai):

        self.ai = ai_core
        self.content = content_ai

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):

        decision = self.ai.decide_next_action()

        if decision["action"] == "WAIT":

            return decision

        product = decision["product"]

        content = self.content.generate(product)

        return {
            "status": "READY_TO_PUBLISH",
            "product": product,
            "content": content,
            "reason": decision["reason"]
        }
