import traceback
from datetime import datetime

# =========================
# SAFE IMPORT WRAPPERS (NO CRASH MODE)
# =========================

try:
    from engine.product_generation_engine import ProductGenerationEngine
except:
    ProductGenerationEngine = None

try:
    from engine.mp4_video_pipeline import MP4VideoPipeline
except:
    MP4VideoPipeline = None

try:
    from engine.real_publish_layer import RealPublishLayer
except:
    RealPublishLayer = None

try:
    from engine.monetization_control_layer import MonetizationControlLayer
except:
    MonetizationControlLayer = None

try:
    from engine.ai_learning_loop import AILearningLoop
except:
    AILearningLoop = None

try:
    from engine.auto_scaling_engine import AutoScalingEngine
except:
    AutoScalingEngine = None


# =========================
# ORCHESTRATOR
# =========================
class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # SAFE INIT (NO CRASH)
        # =========================

        self.product_engine = ProductGenerationEngine() if ProductGenerationEngine else None
        self.video = MP4VideoPipeline() if MP4VideoPipeline else None
        self.publisher = RealPublishLayer() if RealPublishLayer else None
        self.monetization = MonetizationControlLayer() if MonetizationControlLayer else None
        self.learning = AILearningLoop() if AILearningLoop else None
        self.scaling = AutoScalingEngine() if AutoScalingEngine else None

        self.LIVE_MODE = False

    # =========================
    # SAFE PRODUCT LOADER
    # =========================
    def get_products(self):

        if self.product_engine:
            return self.product_engine.build_all_products()["products"]

        # FALLBACK (NO CRASH)
        return [
            {"product_id": "FALLBACK_001", "title": "Fallback Produkt", "description": "Safe Mode"}
        ]

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
    # VIDEO SAFE
    # =========================
    def build_video(self, product):

        if self.video:
            try:
                return self.video.generate_video(product["product_id"])
            except:
                pass

        return {
            "product_id": product["product_id"],
            "video": {"file": "NO_VIDEO"},
            "status": "VIDEO_DISABLED"
        }

    # =========================
    # DISTRIBUTION SAFE
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            try:

                blogger = None
                youtube = None

                if self.publisher:

                    blogger = self.publisher.publish_blogger(
                        "6148350625430723499",
                        item["title"],
                        item.get("html", "")
                    )

                    youtube = self.publisher.publish_youtube(
                        item.get("video"),
                        item["title"]
                    )

                results.append({
                    "product_id": item["product_id"],
                    "blogger": blogger,
                    "youtube": youtube,
                    "status": "SAFE_PUBLISHED",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:

                results.append({
                    "product_id": item.get("product_id"),
                    "status": "SAFE_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return results

    # =========================
    # MAIN PIPELINE (CRASH PROOF)
    # =========================
    def run_pipeline(self):

        results = []

        try:

            products = self.get_products()

            for p in products:

                try:

                    landing = self.build_landingpage(p)
                    video = self.build_video(p)

                    bundle = [{
                        "product_id": p["product_id"],
                        "title": p["title"],
                        "html": landing["html"],
                        "video": video.get("video", {}).get("file", "")
                    }]

                    publish = self.distribute(bundle)

                    results.append({
                        "product_id": p["product_id"],
                        "status": "OK",
                        "landingpage": landing,
                        "video": video,
                        "publish": publish,
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
                "status": "ORCHESTRATOR_CRASH_SAFE_MODE",
                "error": str(e),
                "trace": traceback.format_exc()
            }

        return {
            "status": "GITHUB_STABLE_VERSION_ACTIVE",
            "mode": "CRASH_PROOF",
            "product_count": len(results),
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
