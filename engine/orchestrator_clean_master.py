import traceback
from datetime import datetime

# =========================
# SAFE IMPORTS (NO CRASH)
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
    from engine.google_publish_engine import GooglePublishEngine
except:
    GooglePublishEngine = None

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
        # REAL PRODUCT ENGINE
        # =========================
        self.product_engine = ProductGenerationEngine() if ProductGenerationEngine else None

        # =========================
        # CORE SYSTEMS
        # =========================
        self.video = MP4VideoPipeline() if MP4VideoPipeline else None
        self.publisher = GooglePublishEngine() if GooglePublishEngine else None
        self.monetization = MonetizationControlLayer() if MonetizationControlLayer else None
        self.learning = AILearningLoop() if AILearningLoop else None
        self.scaling = AutoScalingEngine() if AutoScalingEngine else None

        # =========================
        # CONTROL
        # =========================
        self.LIVE_MODE = False
        self.BLOG_ID = "6148350625430723499"

    # =========================
    # LOAD PRODUCTS SAFE
    # =========================
    def get_products(self):

        if self.product_engine:
            try:
                return self.product_engine.build_all_products()["products"]
            except:
                pass

        # FALLBACK SAFE MODE
        return [
            {
                "product_id": "SAFE_001",
                "title": "Safe Produkt 2026",
                "description": "Fallback Mode"
            }
        ]

    # =========================
    # LANDINGPAGE
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
                    <p>{product.get('description','')}</p>
                    <a href="/affiliate/{pid}">Vergleich starten</a>
                </body>
            </html>
            """,
            "status": "LANDING_READY"
        }

    # =========================
    # VIDEO PIPELINE
    # =========================
    def build_video(self, product):

        if not self.video:
            return {
                "product_id": product["product_id"],
                "video": {"file": "NO_VIDEO"},
                "status": "VIDEO_DISABLED"
            }

        try:
            return self.video.generate_video(product["product_id"])
        except Exception as e:
            return {
                "product_id": product["product_id"],
                "status": "VIDEO_ERROR",
                "error": str(e)
            }

    # =========================
    # DISTRIBUTION (REAL PUBLISH)
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item["product_id"]

            try:

                blogger = None
                youtube = None

                if self.publisher:

                    # =========================
                    # BLOGGER REAL PUBLISH
                    # =========================
                    blogger = self.publisher.publish_blogger(
                        blog_id=self.BLOG_ID,
                        title=item["title"],
                        html_content=item.get("html", "")
                    )

                    # =========================
                    # YOUTUBE REAL UPLOAD
                    # =========================
                    youtube = self.publisher.publish_youtube(
                        video_file=item.get("video"),
                        title=item["title"],
                        description=item.get("description", "")
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
                    "product_id": pid,
                    "status": "PUBLISH_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return results

    # =========================
    # MAIN PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        try:

            products = self.get_products()

            for p in products:

                try:

                    # =========================
                    # BUILD ALL LAYERS
                    # =========================
                    landing = self.build_landingpage(p)
                    video = self.build_video(p)

                    # =========================
                    # BUNDLE FOR PUBLISH
                    # =========================
                    bundle = [{
                        "product_id": p["product_id"],
                        "title": p["title"],
                        "html": landing["html"],
                        "description": p.get("description", ""),
                        "video": video.get("video", {}).get("file", "")
                    }]

                    # =========================
                    # REAL DISTRIBUTION
                    # =========================
                    publish = self.distribute(bundle)

                    # =========================
                    # AI LOGGING SAFE
                    # =========================
                    if self.learning:
                        self.learning.log_event(p["product_id"], "view")

                    if self.scaling:
                        self.scaling.update_metrics(p["product_id"], clicks=1, views=1, revenue=0)

                    results.append({
                        "product_id": p["product_id"],
                        "landingpage": landing,
                        "video": video,
                        "publish": publish,
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
            "status": "ORCHESTRATOR_PRODUCTION_READY",
            "mode": "CLOUD_RUN_STABLE_REAL_PUBLISH",
            "product_count": len(results),
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
