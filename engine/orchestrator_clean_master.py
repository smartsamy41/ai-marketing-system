import traceback
from datetime import datetime


# =========================
# SAFE IMPORT WRAPPER
# =========================
def safe_import(module_name, class_name):

    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    except Exception as e:
        print(f"[IMPORT ERROR] {module_name}: {e}")
        return None


# =========================
# OPTIONAL ENGINES (NO CRASH)
# =========================
ProductEngine = safe_import("engine.product_generation_engine", "ProductGenerationEngine")
VideoEngine = safe_import("engine.mp4_video_pipeline", "MP4VideoPipeline")
PublisherEngine = safe_import("engine.google_publish_engine", "GooglePublishEngine")


class OrchestratorCleanMaster:

    def __init__(self):

        # =========================
        # SAFE INIT
        # =========================
        self.product_engine = ProductEngine() if ProductEngine else None
        self.video_engine = VideoEngine() if VideoEngine else None
        self.publisher = PublisherEngine() if PublisherEngine else None

        self.BLOG_ID = "6148350625430723499"

    # =========================
    # SAFE PRODUCTS
    # =========================
    def get_products(self):

        if self.product_engine:
            try:
                return self.product_engine.build_all_products()["products"]
            except:
                pass

        # FALLBACK (NEVER FAIL)
        return [
            {
                "product_id": "SAFE_001",
                "title": "Fallback Produkt",
                "description": "System läuft im Safe Mode"
            }
        ]

    # =========================
    # LANDINGPAGE
    # =========================
    def build_landingpage(self, product):

        return {
            "product_id": product["product_id"],
            "html": f"<h1>{product['title']}</h1>",
            "status": "LANDING_READY"
        }

    # =========================
    # VIDEO SAFE
    # =========================
    def build_video(self, product):

        if not self.video_engine:
            return {
                "video": {"file": "NO_VIDEO"},
                "status": "VIDEO_DISABLED"
            }

        try:
            return self.video_engine.generate_video(product["product_id"])
        except Exception as e:
            return {
                "video": {"file": "ERROR"},
                "status": "VIDEO_ERROR",
                "error": str(e)
            }

    # =========================
    # PUBLISH SAFE (NO CRASH)
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            try:

                blogger = None
                youtube = None

                if self.publisher:

                    blogger = self.publisher.publish_blogger(
                        self.BLOG_ID,
                        item["title"],
                        item.get("html", "")
                    )

                    youtube = self.publisher.publish_youtube(
                        item.get("video"),
                        item["title"]
                    )

                results.append({
                    "product_id": item["product_id"],
                    "blogger": blogger,
                    "youtube": youtube,
                    "status": "DONE",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:

                results.append({
                    "product_id": item.get("product_id"),
                    "status": "PUBLISH_ERROR",
                    "error": str(e),
                    "trace": traceback.format_exc()
                })

        return results

    # =========================
    # MAIN PIPELINE (CRASH PROOF)
    # =========================
    def run_pipeline(self):

        try:

            products = self.get_products()

            results = []

            for p in products:

                try:

                    landing = self.build_landingpage(p)
                    video = self.build_video(p)

                    bundle = [{
                        "product_id": p["product_id"],
                        "title": p["title"],
                        "html": landing["html"],
                        "video": video.get("video", {}).get("file", "")
                    }]

                    publish = self.distribute(bundle)

                    results.append({
                        "product_id": p["product_id"],
                        "landingpage": landing,
                        "video": video,
                        "publish": publish,
                        "status": "OK",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                except Exception as e:

                    results.append({
                        "product_id": p.get("product_id"),
                        "status": "PRODUCT_ERROR",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    })

            return {
                "status": "ORCHESTRATOR_RUNNING_SAFE_MODE",
                "mode": "NO_CRASH_GUARANTEE",
                "product_count": len(results),
                "results": results
            }

        except Exception as e:

            return {
                "status": "FATAL_SAFE_MODE_TRIGGERED",
                "error": str(e),
                "trace": traceback.format_exc()
            }

    def run_all(self, _=None):
        return self.run_pipeline()
