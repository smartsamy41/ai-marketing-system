import traceback
from datetime import datetime

# =========================
# CORE ENGINES
# =========================
from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor
from engine.monetization_control_layer import MonetizationControlLayer


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
        # VIDEO ENGINE
        # =========================
        self.video = MP4VideoPipeline()

        # =========================
        # DISTRIBUTION ENGINE
        # =========================
        self.distributor = LiveDistributor()

        # =========================
        # MONETIZATION ENGINE (NEW)
        # =========================
        self.monetization = MonetizationControlLayer()

        # =========================
        # CONTROL FLAGS
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

        return {
            "product_id": product_id,
            "html": f"""
            <html>
                <head>
                    <title>{product_id} Vergleich 2026</title>
                </head>
                <body>
                    <h1>{product_id} Vergleich 2026</h1>
                    <a href='/affiliate/{product_id}'>Vergleich starten</a>
                </body>
            </html>
            """,
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

            # =========================
            # SELECTIVE LIVE CONTROL
            # =========================
            live = (pid == self.LIVE_PRODUCT)

            self.distributor.LIVE_MODE = live

            results.append({

                "product_id": pid,

                # =========================
                # BLOGGER
                # =========================
                "blogger": self.distributor.publish_blogger(
                    "6148350625430723499",
                    item["title"],
                    item["html"]
                ),

                # =========================
                # YOUTUBE
                # =========================
                "youtube": self.distributor.publish_youtube(
                    item["video"],
                    item["title"]
                ),

                # =========================
                # PINTEREST
                # =========================
                "pinterest": self.distributor.publish_pinterest(
                    item["title"],
                    item.get("description", "")
                ),

                # =========================
                # MONETIZATION TRACKING (NEW)
                # =========================
                "tracking": self.monetization.track_click(
                    pid,
                    source="orchestrator"
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
    # MAIN PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                # =========================
                # CORE BUILD
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

                results.append({

                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "monetization": monetization,
                    "video": video,
                    "distribution": distribution,

                    # =========================
                    # MONETIZATION REPORT
                    # =========================
                    "monetization_report": self.monetization.get_report(),

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
            "status": "FULL_SYSTEM_ACTIVE",
            "mode": "PRODUCTION_READY",
            "live_product": self.LIVE_PRODUCT,
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
