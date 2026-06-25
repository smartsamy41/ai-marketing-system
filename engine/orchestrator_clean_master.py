from engine.monetization_engine import MonetizationEngine
from engine.publish_engine import PublishEngine
from engine.product_layer import ProductLayer
from engine.real_publish_layer import RealPublishLayer


class OrchestratorCleanMaster:

    def __init__(self):

        self.monetization = MonetizationEngine()
        self.publisher = PublishEngine()
        self.real_publish = RealPublishLayer()
        self.products = ProductLayer()

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
            # LEGACY PUBLISH ROUTING (SAFE)
            # =========================
            legacy_publish = self.publisher.publish(
                product_id,
                monetized_content
            )

            # =========================
            # REAL PUBLISH LAYER (LIVE READY)
            # =========================
            real_publish = self.real_publish.publish_all(
                product_id,
                {
                    "title": f"{product_id} Vergleich 2026",
                    "landing_html": landing_html
                }
            )

            # =========================
            # FINAL OUTPUT
            # =========================
            return {
                "product_id": product_id,

                "content": content,
                "monetization": monetized_content,

                "legacy_publish": legacy_publish,
                "real_publish": real_publish,

                "status": "FULL_PUBLISH_SYSTEM_ACTIVE"
            }

        except Exception as e:

            return {
                "product_id": product_id,
                "status": "FAILED_SAFE",
                "error": str(e)
            }

    # =========================
    # BATCH FLOW (FULL SCALE)
    # =========================
    def run_all(self, _):

        product_list = self.products.get_all_products()

        results = []

        for item in product_list:

            product_id = item["product_id"]

            results.append(self.run(product_id))

        return {
            "status": "BATCH_RUNNING",
            "count": len(results),
            "results": results
        }
