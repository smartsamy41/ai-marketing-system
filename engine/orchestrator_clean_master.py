import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine
from engine.product_generation_engine import ProductGenerationEngine
from engine.keyword_discovery_engine import KeywordDiscoveryEngine
from engine.trend_prediction_engine import TrendPredictionEngine


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # ENGINES
        # =========================
        self.product_engine = ProductGenerationEngine()
        self.keyword_engine = KeywordDiscoveryEngine()
        self.trend_engine = TrendPredictionEngine()

        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()
        self.monetization = MonetizationControlLayer()
        self.learning = AILearningLoop()
        self.scaling = AutoScalingEngine()

        # =========================
        # CONTROL
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "TREND_0001"

    # =========================
    # CORE BUILDERS
    # =========================
    def build_content(self, product):

        return {
            "product_id": product["product_id"],
            "title": product["title"],
            "status": "CONTENT_READY"
        }

    def build_landingpage(self, product):

        return {
            "product_id": product["product_id"],
            "html": f"<h1>{product['title']}</h1>",
            "status": "LANDING_READY"
        }

    def build_monetization(self, product):

        pid = product["product_id"]

        return {
            "product_id": pid,
            "affiliate_link": f"/affiliate/{pid}",
            "status": "MONETIZATION_READY"
        }

    def build_video(self, product):

        return self.video.generate_video(product["product_id"])

    # =========================
    # PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        try:

            # =========================
            # TREND ENGINE FIRST (NEW CORE BRAIN)
            # =========================
            trend_data = self.trend_engine.detect_trends()
            product_data = self.trend_engine.to_products()

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
                        "trend": p["keyword"],
                        "score": p["score"],

                        "content": content,
                        "landingpage": landing,
                        "monetization": monetization,
                        "video": video,
                        "distribution": distribution,

                        "learning": self.learning.optimize(),
                        "scaling": self.scaling.execute_scaling(),
                        "top_trends": self.trend_engine.top_trends(),

                        "status": "TREND_PIPELINE_OK",
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
                "status": "TREND_ENGINE_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

        return {
            "status": "FULL_TREND_INTELLIGENCE_SYSTEM",
            "mode": "PREDICTIVE_MARKET_AI",
            "trend_count": len(trend_data["trends"]),
            "product_count": len(results),
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
