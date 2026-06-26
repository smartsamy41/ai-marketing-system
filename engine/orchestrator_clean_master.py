from engine.monetization_engine import MonetizationEngine
from engine.publish_engine import PublishEngine
from engine.product_layer import ProductLayer
from engine.real_publish_layer import RealPublishLayer
from engine.video_engine import VideoEngine
from engine.mp4_video_pipeline import MP4VideoPipeline


class OrchestratorCleanMaster:

    def __init__(self):

        self.monetization = MonetizationEngine()
        self.publisher = PublishEngine()
        self.real_publish = RealPublishLayer()
        self.products = ProductLayer()
        self.video_engine = VideoEngine()
        self.mp4 = MP4VideoPipeline()

    # =========================
    # SINGLE PRODUCT FLOW
    # =========================
    def run(self, product_id):

        try:

            product = {"product_id": product_id}

            # CORE
            content = {
                "product_id": product_id,
                "title": f"{product_id} Vergleich 2026",
                "status": "CORE_ACTIVE"
            }

            # MONETIZATION
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

            # VIDEO ENGINE (LOGIC)
            video_package = self.video_engine.build_video(product_id)

            # MP4 PIPELINE (REAL VIDEO)
            mp4_video = self.mp4.generate_video(product_id)

            # PUBLISH
            legacy_publish = self.publisher.publish(product_id, monetized_content)

            real_publish = self.real_publish.publish_all(
                product_id,
                {"title": content["title"], "landing_html": landing_html}
            )

            return {
                "product_id": product_id,
                "content": content,
                "monetization": monetized_content,

                "video_logic": video_package,
                "mp4_video": mp4_video,

                "legacy_publish": legacy_publish,
                "real_publish": real_publish,

                "status": "FULL_MP4_VIDEO_PIPELINE_ACTIVE"
            }

        except Exception as e:

            return {
                "product_id": product_id,
                "status": "FAILED_SAFE",
                "error": str(e)
            }

    def run_all(self, _):

        product_list = self.products.get_all_products()

        return {
            "status": "BATCH_RUNNING",
            "results": [self.run(p["product_id"]) for p in product_list]
        }
