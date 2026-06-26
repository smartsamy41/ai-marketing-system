import os
import traceback
from datetime import datetime

# =========================
# SAFE CLOUD RUN MODE
# =========================
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# =========================
# CORE ENGINE IMPORTS
# =========================
from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine
from engine.product_generation_engine import ProductGenerationEngine


# =========================
# ORCHESTRATOR CLASS
# =========================
class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # SAFE INIT (NO NETWORK CALLS HERE)
        # =========================
        self.product_engine = ProductGenerationEngine()

        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()
        self.monetization = MonetizationControlLayer()
        self.learning = AILearningLoop()
        self.scaling = AutoScalingEngine()

        # =========================
        # CONTROL FLAGS
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "CHK24_001"

    # =========================
    # CONTENT BUILDER
    # =========================
    def build_content(self, product):

        return {
            "product_id": product["product_id"],
            "title": product["title"],
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE BUILDER
    # =========================
    def build_landingpage(self, product):

        pid = product["product_id"]

        return {
            "product_id": pid,
            "html": f"""
            <html>
                <head>
                    <title>{product['title']}</title>
                </head>
                <body>
                    <h1>{product['title']}</h1>
                    <p>{product.get('description', '')}</p>
                    <a href="/affiliate/{pid}">Vergleich starten</a>
                </body>
            </html>
            """,
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
    # VIDEO PIPELINE
    # =========================
    def build_video(self, product):

        try:
            return self.video.generate_video(product["product_id"])

        except Exception as e:

            return {
                "product_id": product["product_id"],
                "status": "VIDEO_FAILED",
                "error": str(e)
            }

    # =========================
    # DISTRIBUTION (SAFE CALL WRAPPER)
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            try:

                pid = item["product_id"]

                blogger = self.distributor.publish_blogger(
                    "6148350625430723499",
                    item["title"],
                    item.get("html", "")
                )

                youtube = self.distributor.publish_youtube(
                    item.get("video"),
                    item["title"]
                )

                results.append({
                    "product_id": pid,
                    "blogger": blogger,
                    "youtube": youtube,
                    "status": "PUBLISHED",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:

                results.append({
                    "product_id": item.get("product_id"),
                    "status": "DISTRIBUTION_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return results

    # =========================
    # MAIN PIPELINE (SAFE ENTRY POINT)
    # =========================
    def run_pipeline(self):

        results = []

        try:

            # =========================
            # LOAD REAL PRODUCTS ONLY
            # =========================
            products = self.product_engine.build_all_products()["products"]

            for p in products:

                try:

                    # =========================
                    # BUILD ALL LAYERS
                    # =========================
                    content = self.build_content(p)
                    landing = self.build_landingpage(p)
                    monetization = self.build_monetization(p)
                    video = self.build_video(p)

                    # =========================
                    # BUNDLE
                    # =========================
                    bundle = [{
                        "product_id": p["product_id"],
                        "title": p["title"],
                        "html": landing["html"],
                        "video": video.get("video", {}).get("file", "")
                    }]

                    # =========================
                    # DISTRIBUTION
                    # =========================
                    distribution = self.distribute(bundle)

                    # =========================
                    # AI LOGGING (SAFE)
                    # =========================
                    self.learning.log_event(p["product_id"], "view")
                    self.scaling.update_metrics(p["product_id"], clicks=1, views=1, revenue=0)

                    results.append({
                        "product_id": p["product_id"],
                        "content": content,
                        "landingpage": landing,
                        "monetization": monetization,
                        "video": video,
                        "distribution": distribution,
                        "status": "PIPELINE_OK",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                except Exception as e:

                    results.append({
                        "product_id": p.get("product_id"),
                        "status": "PRODUCT_ERROR",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    })

        except Exception as e:

            return {
                "status": "ORCHESTRATOR_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

        return {
            "status": "ORCHESTRATOR_SAFE_MODE_ACTIVE",
            "mode": "CLOUD_RUN_STABLE",
            "product_count": len(results),
            "results": results
        }

    # =========================
    # COMPATIBILITY WRAPPER
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
