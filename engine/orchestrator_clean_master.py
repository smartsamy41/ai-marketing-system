from engine.monetization_engine import MonetizationEngine


class OrchestratorCleanMaster:

    def __init__(self):
        self.monetization = MonetizationEngine()

    def run(self, product_id):

        try:

            product = {"product_id": product_id}

            # =========================
            # CORE DATA (SAFE)
            # =========================
            content = {
                "product_id": product_id,
                "title": f"{product_id} Vergleich 2026",
                "status": "CORE_ACTIVE"
            }

            # =========================
            # MONETIZATION LAYER
            # =========================
            landing_html = self.monetization.build_landing_html(product)
            affiliate_link = self.monetization.build_affiliate_link(product_id)
            pinterest = self.monetization.build_pinterest(product)
            youtube_script = self.monetization.build_youtube_script(product)

            # =========================
            # FINAL OUTPUT
            # =========================
            return {
                "product_id": product_id,
                "content": content,

                "landingpage_html": landing_html,
                "affiliate_link": affiliate_link,

                "pinterest": pinterest,
                "youtube": youtube_script,

                "status": "MONETIZATION_CONNECTED"
            }

        except Exception as e:

            return {
                "product_id": product_id,
                "status": "FAILED_SAFE",
                "error": str(e)
            }

    def run_all(self, products):

        return [self.run(p) for p in products]
