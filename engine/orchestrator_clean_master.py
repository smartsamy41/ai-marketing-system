import traceback
from datetime import datetime

# =========================
# CORE ENGINES (REAL ONLY)
# =========================
from engine.product_generation_engine import ProductGenerationEngine
from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.real_publish_layer import RealPublishLayer
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # REAL PRODUCT SOURCE ONLY
        # =========================
        self.product_engine = ProductGenerationEngine()

        # =========================
        # CORE SYSTEMS
        # =========================
        self.video = MP4VideoPipeline()
        self.publisher = RealPublishLayer()
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
            "description": product.get("description", ""),
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE BUILDER
    # =========================
    def build_landingpage(self, product):

        pid = product["product_id"]

        html = f"""
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
        """

        return {
            "product_id": pid,
            "html": html,
            "status": "LANDING_READY"
        }

    # =========================
    # VIDEO PIPELINE
    # =========================
    def build_video(self, product):

        return self.video.generate_video(product["product_id"])

    # =========================
    # DISTRIBUTION (REAL PUBLISH)
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item["product_id"]

            try:

                # =========================
                # BLOGGER REAL PUBLISH
                # =========================
                blogger = self.publisher.publish_blogger(
                    blog_id="6148350625430723499",
                    title=item["title"],
                    content=item.get("html", "")
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
                    "status": "REAL_PUBLISHED",
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

            # =========================
            # LOAD REAL PRODUCTS ONLY
            # =========================
            products_data = self.product_engine.build_all_products()
            products = products_data["products"]

            for p in products:

                try:

                    # =========================
                    # BUILD LAYERS
                    # =========================
                    content = self.build_content(p)
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
                        "video": video["video"]["file"]
                    }]

                    # =========================
                    # REAL DISTRIBUTION
                    # =========================
                    publish = self.distribute(bundle)

                    # =========================
                    # MONITORING
                    # =========================
                    self.learning.log_event(p["product_id"], "view")
                    self.scaling.update_metrics(p["product_id"], clicks=1, views=1, revenue=0)

                    results.append({
                        "product_id": p["product_id"],
                        "content": content,
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
            "status": "PRODUCTION_ORCHESTRATOR_ACTIVE",
            "mode": "REAL_PUBLISH_ENABLED",
            "product_count": len(results),
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
