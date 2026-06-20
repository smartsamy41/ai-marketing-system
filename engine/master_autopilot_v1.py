from datetime import datetime


def _now():
    return str(datetime.now())


# =========================
# MASTER AUTOPILOT
# =========================

def run_master_autopilot(
    products,
    auto_system,
    video_engine,
    upload_engine,
    video_folder
):

    print("🟢 MASTER AUTOPILOT STARTED")

    try:

        # =========================
        # FULL PIPELINE RUN
        # =========================

        result = auto_system.run(
            products=products,
            video_engine=video_engine,
            upload_engine=upload_engine,
            video_folder=video_folder
        )

        # =========================
        # SYSTEM SUMMARY
        # =========================

        summary = {
            "status": "MASTER_AUTOPILOT_DONE",
            "time": _now(),
            "products_processed": len(products),
            "videos_created": 0,
            "uploads": 0,
            "raw_result": result
        }

        # extract stats safely
        try:
            for r in result.get("results", []):

                if r.get("video", {}).get("status") == "VIDEO_RENDERED":
                    summary["videos_created"] += 1

                if "youtube" in str(r.get("upload", {})):
                    summary["uploads"] += 1

        except:
            pass

        print("🟢 MASTER AUTOPILOT FINISHED")

        return summary

    except Exception as e:

        return {
            "status": "AUTOPILOT_ERROR",
            "error": str(e),
            "time": _now()
        }


# =========================
# WRAPPER CLASS
# =========================

class MasterAutopilotV1:

    def __init__(self):
        print("🟢 MASTER AUTOPILOT V1 READY")

    def run(self, products, auto_system, video_engine, upload_engine, video_folder):
        return run_master_autopilot(
            products,
            auto_system,
            video_engine,
            upload_engine,
            video_folder
        )
