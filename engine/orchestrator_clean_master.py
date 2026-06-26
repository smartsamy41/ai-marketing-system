import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # FIXED PRODUCT SET
        # =========================
        self.products = [
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]

        # =========================
        # VIDEO PIPELINE (YOUR FILE)
        # =========================
        self.video = MP4VideoPipeline()

    # =========================
    # CONTENT ENGINE (SAFE MOCK)
    # =========================
    def build_content(self, product_id):

        return {
            "product_id": product_id,
            "title": f"{product_id} Vergleich 2026",
            "status": "CONTENT_READY"
        }

    # =========================
    # LANDINGPAGE ENGINE (SAFE MOCK)
    # =========================
    def build_landingpage(self, product_id):

        html = f"""
        <html>
            <head>
                <title>{product_id} Vergleich 2026</title>
            </head>
            <body>
                <h1>{product_id} Vergleich 2026</h1>
                <p>Vergleich starten für {product_id}</p>
                <a href="/affiliate/{product_id}">Jetzt vergleichen</a>
            </body>
        </html>
        """

        return {
            "product_id": product_id,
            "html": html,
            "status": "LANDING_READY"
        }

    # =========================
    # MONETIZATION LAYER (SAFE MOCK)
    # =========================
    def build_monetization(self, product_id):

        return {
            "product_id": product_id,
            "affiliate_link": f"/affiliate/{product_id}",
            "pinterest": {
                "title": f"{product_id} sparen & vergleichen 2026",
                "status": "PIN_READY"
            },
            "youtube": {
                "title": f"{product_id} Vergleich 2026",
                "status": "SCRIPT_READY"
            }
        }

    # =========================
    # VIDEO PIPELINE (REAL FFmpeg FILE SYSTEM)
    # =========================
    def build_video(self, product_id):

        return self.video.generate_video(product_id)

    # =========================
    # FULL PIPELINE PER PRODUCT
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                content = self.build_content(p)
                landing = self.build_landingpage(p)
                monetization = self.build_monetization(p)
                video = self.build_video(p)

                results.append({
                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "monetization": monetization,
                    "video": video,
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
            "mode": "CLEAN_ORCHESTRATOR_FINAL",
            "results": results
        }

    # =========================
    # COMPATIBILITY LAYER
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
