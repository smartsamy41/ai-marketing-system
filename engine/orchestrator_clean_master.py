import traceback
from datetime import datetime

from engine.mp4_video_pipeline import MP4VideoPipeline
from engine.live_distributor import LiveDistributor


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # REAL PRODUCTS ONLY
        # =========================
        self.products = self.load_real_products()

        self.video = MP4VideoPipeline()
        self.distributor = LiveDistributor()

    # =========================
    # REAL PRODUCT SOURCE (NO AI)
    # =========================
    def load_real_products(self):

        return [
            # =========================
            # CHECK24
            # =========================
            {
                "product_id": "CHK24_001",
                "title": "Strom Vergleich 2026",
                "type": "check24"
            },
            {
                "product_id": "CHK24_002",
                "title": "Gas Vergleich 2026",
                "type": "check24"
            },
            {
                "product_id": "CHK24_003",
                "title": "DSL Vergleich 2026",
                "type": "check24"
            },

            # =========================
            # TARIFCHECK
            # =========================
            {
                "product_id": "TC_001",
                "title": "Solaranlage Vergleich 2026",
                "type": "tarifcheck"
            },
            {
                "product_id": "TC_002",
                "title": "Kfz Versicherung Vergleich 2026",
                "type": "tarifcheck"
            },

            # =========================
            # AMAZON (REAL PRODUCTS ONLY)
            # =========================
            {
                "product_id": "AMZ_001",
                "title": "Amazon Bestseller Produkt 2026",
                "type": "amazon"
            },
            {
                "product_id": "AMZ_002",
                "title": "Amazon Technik Deal 2026",
                "type": "amazon"
            },

            # =========================
            # TELEKOM (DIRECT ONLY)
            # =========================
            {
                "product_id": "TELEKOM_001",
                "title": "Telekom Internet Angebot",
                "type": "telekom_direct"
            }
        ]

    # =========================
    # LANDINGPAGE ENGINE
    # =========================
    def build_landingpage(self, product):

        pid = product["product_id"]

        # TELEKOM = NO LANDINGPAGE (DIRECT LINK ONLY)
        if product["type"] == "telekom_direct":

            return {
                "product_id": pid,
                "type": "redirect",
                "url": "https://www.telekom.de/",
                "status": "DIRECT_LINK_ONLY"
            }

        html = f"""
        <html>
            <head>
                <title>{product['title']}</title>
            </head>

            <body>
                <h1>{product['title']}</h1>

                <p>{product['title']} jetzt vergleichen und passende Angebote finden.</p>

                <a href="/affiliate/{pid}">
                    👉 Vergleich starten
                </a>
            </body>
        </html>
        """

        return {
            "product_id": pid,
            "html": html,
            "status": "LANDING_READY"
        }

    # =========================
    # VIDEO ENGINE
    # =========================
    def build_video(self, product):

        return self.video.generate_video(product["product_id"])

    # =========================
    # DISTRIBUTION ENGINE
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            pid = item["product_id"]

            blogger = self.distributor.publish_blogger(
                "6148350625430723499",
                item["title"],
                item.get("html", "")
            )

            youtube = self.distributor.publish_youtube(
                item.get("video"),
                item["title"]
            )

            results.append({
                "product_id": pid,
                "blogger": blogger,
                "youtube": youtube,
                "status": "PUBLISHED",
                "timestamp": datetime.utcnow().isoformat()
            })

        return results

    # =========================
    # MAIN PIPELINE
    # =========================
    def run_pipeline(self):

        results = []

        for p in self.products:

            try:

                landing = self.build_landingpage(p)
                video = self.build_video(p)

                bundle = [{
                    "product_id": p["product_id"],
                    "title": p["title"],
                    "html": landing.get("html", ""),
                    "video": video["video"]["file"]
                }]

                publish = self.distribute(bundle)

                results.append({
                    "product_id": p["product_id"],
                    "type": p["type"],
                    "landingpage": landing,
                    "video": video,
                    "publish": publish,
                    "status": "DONE",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:

                results.append({
                    "product_id": p["product_id"],
                    "status": "ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return {
            "status": "FINAL_REAL_PRODUCT_SYSTEM",
            "mode": "CHECK24 + TARIFCHECK + AMAZON + TELEKOM",
            "results": results
        }

    def run_all(self, _=None):
        return self.run_pipeline()
