from engine.monetization_engine import MonetizationEngine
from engine.publish_engine import PublishEngine


class OrchestratorCleanMaster:

    def __init__(self):

        self.monetization = MonetizationEngine()
        self.publisher = PublishEngine()

    # =========================
    # SINGLE PRODUCT FLOW
    # =========================
    def run(self, product_id):

        try:

            product = {"product_id": product_id}

            # =========================
            # CORE CONTENT
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

            monetized_content = {
                "landing_html": landing_html,
                "affiliate_link": affiliate_link,
                "pinterest": pinterest,
                "youtube": youtube_script
            }

            # =========================
            # PUBLISH LAYER (NEW)
            # =========================
            publish_result = self.publisher.publish(
                product_id,
                monetized_content
            )

            # =========================
            # FINAL OUTPUT
            # =========================
            return {
                "product_id": product_id,
                "content": content,
                "monetization": monetized_content,
                "publish": publish_result,
                "status": "FULL_SYSTEM_ACTIVE"
            }

        except Exception as e:

            return {
                "product_id": product_id,
                "status": "FAILED_SAFE",
                "error": str(e)
            }

    # =========================
    # BATCH FLOW
    # =========================
    def run_all(self, products):

        return [self.run(p) for p in products]
