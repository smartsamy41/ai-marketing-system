import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # PRODUCTS
        # =========================
        self.products = [
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]

        # =========================
        # ENGINES
        # =========================
        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()
        self.monetization = MonetizationControlLayer()
        self.learning = AILearningLoop()
        self.scaling = AutoScalingEngine()

        # =========================
        # CONTROL
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "CHK24_001"

    # =========================
    # CORE BUILDERS
    # =========================
    def build_content(self, product_id):
        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "status": "CONTENT_READY"
        }

    def build_landingpage(self, product_id):
        return {
            "product_id": product_id,
            "html": f"<h1>{product_id} Vergleich 2026</h1>",
            "status": "LANDING_READY"
        }

    def build_monetization(self, product_id):
        return {
            "product_id": product_id,
            "affiliate_link": f"/affiliate/{product_id}",
            "status": "MONETIZATION_READY"
        }

    def build_video(self, product_id):
        return self.video.generate_video(product_id)

    # =========================
    # DISTRIBUTION
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item["product_id"]

            live = (pid == self.LIVE_PRODUCT)
            self.distributor.LIVE_MODE = live

            # =========================
            # LEARNING DATA FEED
            # =========================
            self.learning.log_event(pid, "view")
            self.learning.log_event(pid, "click")
            self.learning.log_event(pid, "video")

            # =========================
            # SCALING FEED
            # =========================
            self.scaling.update_metrics(
                pid,
                clicks=1,
                views=1,
                revenue=0
            )

            results.append({
                "product_id": pid,

                "blogger": self.distributor.publish_blogger(
                    "6148350625430723499",
                    item["title"],
                    item["html"]
                ),

                "youtube": self.distributor.publish_youtube(
                    item["video"],
                    item["title"]
                ),

                "pinterest": self.distributor.publish_pinterest(
                    item["title"],
                    item.get("description", "")
                ),

                "live_mode": live,
                "status": "DISTRIBUTED_OK",
                "timestamp": datetime.utcnow().isoformat()
            })

        return {
            "status": "DISTRIBUTION_DONE",
            "results": results
        }

    # =========================
    # PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                content = self.build_content(p)
                landing = self.build_landingpage(p)
                monetization = self.build_monetization(p)
                video = self.build_video(p)

                bundle = [{
                    "product_id": p,
                    "title": content["title"],
                    "html": landing["html"],
                    "description": "auto system content",
                    "video": video["video"]["file"]
                }]

                distribution = self.distribute(bundle)

                results.append({
                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "monetization": monetization,
                    "video": video,
                    "distribution": distribution,

                    # =========================
                    # AI SYSTEM OUTPUTS
                    # =========================
                    "ai_learning": self.learning.optimize(),
                    "scaling": self.scaling.execute_scaling(),

                    "status": "FULL_AI_SYSTEM_ACTIVE",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:

                results.append({
                    "product_id": p,
                    "status": "ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return {
            "status": "AUTONOMOUS_SYSTEM_ACTIVE",
            "mode": "SELF_SCALING_AI",
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
