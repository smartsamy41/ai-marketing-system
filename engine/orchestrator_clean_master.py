import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor


class OrchestratorCleanMaster:

    def __init__(self):

        self.products = [
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]

        # =========================
        # SELECTIVE LIVE CONTROL
        # =========================
        self.LIVE_MODE = False
        self.LIVE_PRODUCT = "CHK24_001"   # 🔥 ONLY THIS PRODUCT GOES LIVE

        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()

    # =========================
    # CONTENT
    # =========================
    def build_content(self, product_id):

        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE
    # =========================
    def build_landingpage(self, product_id):

        return {
            "product_id": product_id,
            "html": f"<h1>{product_id} Vergleich 2026</h1>",
            "status": "LANDING_READY"
        }

    # =========================
    # MONETIZATION
    # =========================
    def build_monetization(self, product_id):

        return {
            "product_id": product_id,
            "affiliate_link": f"/affiliate/{product_id}",
            "status": "MONETIZATION_READY"
        }

    # =========================
    # VIDEO
    # =========================
    def build_video(self, product_id):

        return self.video.generate_video(product_id)

    # =========================
    # SELECTIVE DISTRIBUTION LOGIC
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item.get("product_id")

            # =========================
            # SELECTIVE LIVE RULE
            # =========================
            if pid == self.LIVE_PRODUCT:
                live = True
            else:
                live = False

            distributor = self.distributor
            distributor.LIVE_MODE = live

            results.append({
                "product_id": pid,

                "blogger": distributor.publish_blogger(
                    "6148350625430723499",
                    item.get("title"),
                    item.get("html")
                ),

                "youtube": distributor.publish_youtube(
                    item.get("video"),
                    item.get("title")
                ),

                "pinterest": distributor.publish_pinterest(
                    item.get("title"),
                    item.get("description")
                ),

                "live_mode": live,
                "status": "SELECTIVE_OK",
                "timestamp": datetime.utcnow().isoformat()
            })

        return {
            "status": "SELECTIVE_LIVE_ACTIVE",
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

                content = self.build_content(p)
                landing = self.build_landingpage(p)
                monetization = self.build_monetization(p)
                video = self.build_video(p)

                bundle = [{
                    "product_id": p,
                    "title": content["title"],
                    "html": landing["html"],
                    "description": "auto generated",
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
            "status": "SELECTIVE_PIPELINE_DONE",
            "live_product": self.LIVE_PRODUCT,
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
