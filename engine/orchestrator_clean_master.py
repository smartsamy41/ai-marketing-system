import traceback
from datetime import datetime

# =========================
# ENGINES IMPORT
# =========================
from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop
from engine.auto_scaling_engine import AutoScalingEngine
from engine.product_generation_engine import ProductGenerationEngine


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # PRODUCT GENERATION ENGINE (NEW)
        # =========================
        self.product_engine = ProductGenerationEngine()

        # =========================
        # CORE ENGINES
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
        self.LIVE_PRODUCT = "STROM_001"

    # =========================
    # CONTENT ENGINE
    # =========================
    def build_content(self, product):

        return {
            "product_id": product["product_id"],
            "title": product["title"],
            "html": f"<h1>{product['title']}</h1>",
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE ENGINE
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
                    <p>{product['description']}</p>
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
    # VIDEO
    # =========================
    def build_video(self, product):

        return self.video.generate_video(product["product_id"])

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
            # AI LEARNING FEED
            # =========================
            self.learning.log_event(pid, "view")
            self.learning.log_event(pid, "click")
            self.learning.log_event(pid, "video")

            # =========================
            # SCALING FEED
            # =========================
            self.scaling.update_metrics(pid, clicks=1, views=1, revenue=0)

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

        try:

            # =========================
            # PRODUCT GENERATION (NEW CORE)
            # =========================
            product_data = self.product_engine.build_all_products()
            products = product_data["products"]

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
                        "title": content["title"],
                        "html": landing["html"],
                        "description": p["description"],
                        "video": video["video"]["file"]
                    }]

                    # =========================
                    # DISTRIBUTION
                    # =========================
                    distribution = self.distribute(bundle)

                    # =========================
                    # MONETIZATION + AI
                    # =========================
                    self.monetization.track_click(p["product_id"], source="landingpage")

                    self.scaling.update_metrics(
                        p["product_id"],
                        clicks=1,
                        views=1,
                        revenue=0
                    )

                    results.append({

                        "product_id": p["product_id"],
                        "category": p["category"],

                        "content": content,
                        "landingpage": landing,
                        "monetization": monetization,
                        "video": video,
                        "distribution": distribution,

                        "learning": self.learning.optimize(),
                        "scaling": self.scaling.execute_scaling(),
                        "monetization_report": self.monetization.get_report(),

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
                "status": "PIPELINE_FAILED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

        return {
            "status": "FULL_DYNAMIC_SYSTEM_ACTIVE",
            "mode": "AUTO_PRODUCT_GENERATION",
            "product_count": len(results),
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
