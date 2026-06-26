import traceback
from datetime import datetime


class OrchestratorCleanMaster:

    def __init__(self):

        self.products = [
            "CHK24_001",
            "TC_001",
            "AMZ_001"
        ]

        # =========================
        # LIVE SWITCH CONTROL
        # =========================
        self.LIVE_MODE = False   # 👈 WICHTIG: SAFE DEFAULT

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

        html = f"""
        <html>
            <head>
                <title>{product_id} Vergleich 2026</title>
            </head>
            <body>
                <h1>{product_id} Vergleich 2026</h1>
                <p>Vergleich starten für {product_id}</p>
                <a href="/affiliate/{product_id}">👉 Jetzt vergleichen</a>
            </body>
        </html>
        """

        return {
            "product_id": product_id,
            "html": html,
            "status": "LANDING_READY"
        }

    # =========================
    # MONETIZATION
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
                "status": "VIDEO_SCRIPT_READY"
            }
        }

    # =========================
    # SAFE PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                content = self.build_content(p)
                landing = self.build_landingpage(p)
                monetization = self.build_monetization(p)

                item = {
                    "product_id": p,
                    "content": content,
                    "landingpage": landing,
                    "monetization": monetization,
                    "status": "PIPELINE_OK",
                    "timestamp": datetime.utcnow().isoformat(),

                    # =========================
                    # LIVE SWITCH LOGIC
                    # =========================
                    "live_publish": self.publish_if_enabled(p, content, landing, monetization)
                }

                results.append(item)

            except Exception as e:

                results.append({
                    "product_id": p,
                    "status": "PIPELINE_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return {
            "status": "PIPELINE_DONE",
            "mode": "LIVE_SWITCH_READY",
            "live_enabled": self.LIVE_MODE,
            "results": results
        }

    # =========================
    # LIVE PUBLISH GATE
    # =========================
    def publish_if_enabled(self, product_id, content, landing, monetization):

        if not self.LIVE_MODE:

            return {
                "status": "SIMULATED",
                "note": "LIVE_MODE is OFF - safe execution only"
            }

        # =========================
        # REAL PUBLISH PLACEHOLDER
        # =========================
        return {
            "status": "LIVE_EXECUTION_ACTIVE",
            "product_id": product_id,
            "blogger": "READY_TO_POST",
            "pinterest": "READY_TO_PIN",
            "youtube": "READY_TO_UPLOAD"
        }

    # =========================
    # COMPATIBILITY
    # =========================
    def run_all(self, _=None):
        return self.run_pipeline()
