from datetime import datetime


# =========================
# CORE ENGINE SAFE LAYER
# =========================
class CoreEngine:

    def __init__(self):
        self.status = "ACTIVE"
        self.start_time = datetime.utcnow()

    def health(self):
        return {
            "status": "OK",
            "engine": "core_engine",
            "time": str(datetime.utcnow())
        }

    def safe_run(self, func, *args, **kwargs):
        try:
            return {
                "status": "SUCCESS",
                "result": func(*args, **kwargs)
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }
