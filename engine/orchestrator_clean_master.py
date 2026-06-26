import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor


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
        # VIDEO PIPELINE
        # =========================
        self.video = MP4VideoPipeline()

        # =========================
        # LIVE DISTRIBUTOR
        # =========================
        self.distributor = LiveDistributor()

    # =========================
    # CONTENT ENGINE
    # =========================
    def build_content(self, product_id):

        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "html": f"<h1>{product_id} Vergleich 2026</h1>",
            "description": f"Beste Angebote für {product_id}",
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
                <p>Jetzt vergleichen für {product_id}</p>
                <a href="/affiliate/{product_id}">👉 Vergleich starten</a>
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
            "pinterest": {
                "title": f"{product_id} sparen & vergleichen 2026",
                "description": f"Beste Tarife für {product_id}",
                "status": "PIN_READY"
            },
            "youtube": {
                "title": f"{product_id} Vergleich 2026",
                "status": "SCRIPT_READY"
            }
        }

    # =========================
    # VIDEO ENGINE
    # =========================
    def build_video(self, product_id):

        return self.video.generate_video(product_id)

    # =========================
    # FULL PIPELINE
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
                # COMBINE OUTPUT
                # =========================
                bundle = {
                    "product_id": p,
                    "title": content["title"],
                    "html": landing["html"],
                    "description": monetization["pinterest"]["description"],
                    "video": video["video"]["file"],
                    "status": "READY_FOR_DISTRIBUTION",
                    "timestamp": datetime.utcnow().isoformat()
                }

                # =========================
                # LIVE DISTRIBUTION STEP
                # =========================
                distribution = self.distributor.distribute([bundle])

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
                    "status": "PIPELINE_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return {
            "status": "DONE",
            "mode": "FULL_SYSTEM_ACTIVE",
            "results": results
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
