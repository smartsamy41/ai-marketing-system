from datetime import datetime


class LiveDistributor:

    def __init__(self):

        self.LIVE_MODE = False  # 🔒 LOCKED DEFAULT

    # =========================
    # BLOGGER
    # =========================
    def publish_blogger(self, blog_id, title, html):

        if not self.LIVE_MODE:
            return {
                "status": "LOCKED_BLOGGER",
                "action": "NO_PUBLISH"
            }

        return {
            "status": "READY_FOR_LIVE_BLOGGER"
        }

    # =========================
    # YOUTUBE
    # =========================
    def publish_youtube(self, video_path, title):

        if not self.LIVE_MODE:
            return {
                "status": "LOCKED_YOUTUBE",
                "action": "NO_UPLOAD"
            }

        return {
            "status": "READY_FOR_YOUTUBE"
        }

    # =========================
    # PINTEREST
    # =========================
    def publish_pinterest(self, title, description):

        return {
            "status": "LOCKED_PINTEREST_QUEUE",
            "action": "NO_PUSH"
        }

    # =========================
    # DISTRIBUTE
    # =========================
    def distribute(self, bundle):

        results = []

        for item in bundle:

            results.append({
                "product_id": item.get("product_id"),
                "blogger": self.publish_blogger(
                    "6148350625430723499",
                    item.get("title"),
                    item.get("html")
                ),
                "youtube": self.publish_youtube(
                    item.get("video"),
                    item.get("title")
                ),
                "pinterest": self.publish_pinterest(
                    item.get("title"),
                    item.get("description")),
                "status": "SAFE_LOCK_ACTIVE",
                "timestamp": datetime.utcnow().isoformat()
            })

        return {
            "status": "DISTRIBUTION_LOCKED",
            "results": results
        }
