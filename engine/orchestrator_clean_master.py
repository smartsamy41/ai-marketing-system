import traceback
from datetime import datetime

# =========================
# ENGINES
# =========================
from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer
from engine.ai_learning_loop import AILearningLoop


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
        # CORE ENGINES
        # =========================
        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()
        self.monetization = MonetizationControlLayer()
        self.learning = AILearningLoop()

        # =========================
        # CONTROL
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "CHK24_001"

    # =========================
    # CONTENT ENGINE
    # =========================
    def build_content(self, product_id):

        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "html": f"<h1>{product_id} Vergleich 2026</h1>",
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE ENGINE
    # =========================
    def build_landingpage(self, product_id):

        html = f"""
        <html>
            <head>
                <title>{product_id} Vergleich 2026</title>
            </head>
            <body>
                <h1>{product_id} Vergleich 2026</h1>
                <a href="/affiliate/{product_id}">Vergleich starten</a>
            </body>
        </html>
        """

        return {
            "product_id": product_id,
            "html": html,
            "status": "LANDING_READY"
        }

    # =========================
    # MONETIZATION ENGINE
    # =========================
    def build_monetization(self, product_id):

        return {
            "product_id": product_id,
            "affiliate_link": f"/affiliate/{product_id}",
            "status": "MONETIZATION_READY"
        }

    # =========================
    # VIDEO ENGINE
    # =========================
    def build_video(self, product_id):
        return self.video.generate_video(product_id)

    # =========================
    # DISTRIBUTION ENGINE
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item["product_id"]

            live = (pid == self.LIVE_PRODUCT)

            self.distributor.LIVE_MODE = live

            # =========================
            # EVENTS (AI LEARNING)
            # =========================
            self.learning.log_event(pid, "view")
            self.learning.log_event(pid, "click")
            self.learning.log_event(pid, "video")

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
            "live_product": self.LIVE_PRODUCT,
            "results": results
        }

    # =========================
    # PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                # =========================
                # BUILD LAYERS
                # =========================
                content = self.build_content(p)
                landing = self.build_landingpage(p)
                monetization = self.build_monetization(p)
                video = self.build_video(p)

                # =========================
                # MONETIZATION TRACKING
                # =========================
                self.monetization.track_click(p, source="landingpage")

                # =========================
                # BUNDLE
                # =========================
                bundle = [{
                    "product_id": p,
                    "title": content["title"],
                    "html": landing["html"],
                    "description": "auto generated system content",
                    "video": video["video"]["file"]
                }]

                # =========================
                # DISTRIBUTION
                # =========================
                distribution = self.distribute(bundle)

                # =========================
                # AI LEARNING OUTPUT
                # =========================
                ai_learning = self.learning.optimize()

                # =========================
                # FINAL RESULT
                # =========================
                results.append({

                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "monetization": monetization,
                    "video": video,
                    "distribution": distribution,

                    "monetization_report": self.monetization.get_report(),
                    "ai_learning": ai_learning,

                    "status": "PIPELINE_OK",
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
            "status": "FULL_AI_SYSTEM_ACTIVE",
            "mode": "SELF_LEARNING_ENGINE",
            "live_product": self.LIVE_PRODUCT,
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
