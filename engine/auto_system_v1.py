from datetime import datetime
import os


# =========================
# TIME
# =========================

def _now():
    return str(datetime.now())


# =========================
# AUTO SYSTEM ENGINE
# =========================

def run_auto_system(
    products,
    video_engine,
    upload_engine,
    video_folder
):

    results = []

    for product in products:

        try:

            product_id = product.get("product_id")

            # =========================
            # 1. VIDEO GENERATION
            # =========================

            video_result = video_engine.run(
                [product],
                video_folder
            )

            # extract file path
            video_file = None

            try:
                video_file = video_result["results"][0]["video"]["file"]["file"]
            except:
                video_file = None

            # =========================
            # 2. UPLOAD TO YOUTUBE
            # =========================

            upload_result = None

            if video_file and os.path.exists(video_file):

                upload_result = upload_engine.upload_from_queue(
                    youtube_results=video_result["results"],
                    video_folder=video_folder
                )

            else:

                upload_result = {
                    "status": "SKIPPED_NO_VIDEO"
                }

            # =========================
            # 3. FINAL LOG
            # =========================

            results.append({
                "product_id": product_id,
                "video": video_result,
                "upload": upload_result,
                "status": "AUTO_DONE",
                "time": _now()
            })

        except Exception as e:

            results.append({
                "product_id": product.get("product_id"),
                "status": "ERROR",
                "error": str(e)
            })

    return {
        "status": "AUTO_SYSTEM_V1_DONE",
        "executed": len(results),
        "results": results,
        "time": _now()
    }


# =========================
# WRAPPER CLASS
# =========================

class AutoSystemV1:

    def __init__(self):
        print("🟢 AUTO SYSTEM V1 READY")

    def run(self, products, video_engine, upload_engine, video_folder):
        return run_auto_system(
            products,
            video_engine,
            upload_engine,
            video_folder
        )
