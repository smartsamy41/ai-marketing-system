import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine
from engine.product_generation_engine import ProductGenerationEngine
from engine.keyword_discovery_engine import KeywordDiscoveryEngine


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # ENGINES
        # =========================
        self.product_engine = ProductGenerationEngine()
        self.keyword_engine = KeywordDiscoveryEngine()

        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()
        self.monetization = MonetizationControlLayer()
        self.learning = AILearningLoop()
        self.scaling = AutoScalingEngine()

        # =========================
        # CONTROL
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "KW_0001"

    # =========================
    # CONTENT
    # =========================
    def build_content(self, product):

        return {
            "product_id": product["product_id"],
            "title": product["title"],
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE
    # =========================
    def build_landingpage(self, product):

        return {
            "product_id": product["product_id"],
            "html": f"<h1>{product['title']}</h1>",
            "status": "LANDING_READY"
        }

    # =========================
    # MONETIZATION
    # =========================
    def build_monetization(self, product):

        pid = product["product_id"]

        return {
            "product_id": pid,
            "affiliate_link": f"/affiliate/{pid}",
            "status": "MONETIZATION_READY"
        }

    # =========================
    # VIDEO
    # =========================
    def build_video(self, product):

        return self.video.generate_video(product["product_id"])

    # =========================
    # PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        try:

            # =========================
            # KEYWORD DISCOVERY FIRST
            # =========================
            keyword_data = self.keyword_engine.discover()
            product_data = self.keyword_engine.to_products()

            products = product_data["products"]

            for p in products:

                try:

                    content = self.build_content(p)
                    landing = self.build_landingpage(p)
                    monetization = self.build_monetization(p)
                    video = self.build_video(p)

                    bundle = [{
                        "product_id": p["product_id"],
                        "title": content["title"],
                        "html": landing["html"],
                        "description": p["keyword"],
                        "video": video["video"]["file"]
                    }]

                    self.distributor.LIVE_MODE = False

                    self.learning.log_event(p["product_id"], "view")
                    self.learning.log_event(p["product_id"], "click")
                    self.learning.log_event(p["product_id"], "video")

                    self.scaling.update_metrics(p["product_id"], clicks=1, views=1, revenue=0)

                    distribution = self.distribute(bundle)

                    results.append({
                        "product_id": p["product_id"],
                        "keyword": p["keyword"],

                        "content": content,
                        "landingpage": landing,
                        "monetization": monetization,
                        "video": video,
                        "distribution": distribution,

                        "learning": self.learning.optimize(),
                        "scaling": self.scaling.execute_scaling(),

                        "status": "KEYWORD_PIPELINE_OK",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                except Exception as e:

                    results.append({
                        "product_id": p.get("product_id"),
                        "status": "ERROR",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    })

        except Exception as e:

            return {
                "status": "KEYWORD_DISCOVERY_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

        return {
            "status": "FULL_KEYWORD_AUTONOMOUS_SYSTEM",
            "mode": "SELF_EXPANDING_MARKET_ENGINE",
            "keyword_count": len(keyword_data["keywords"]),
            "product_count": len(results),
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
