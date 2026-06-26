from datetime import datetime


class LiveDistributor:

    def __init__(self, blogger_service=None, youtube_service=None):
        self.blogger = blogger_service
        self.youtube = youtube_service

        self.LIVE_MODE = False  # SAFE DEFAULT

    # =========================
    # BLOGGER PUBLISH
    # =========================
    def publish_blogger(self, blog_id, title, html):

        if not self.LIVE_MODE:
            return {
                "status": "SIMULATED_BLOGGER",
                "blog_id": blog_id
            }

        try:
            post = self.blogger.posts().insert(
                blogId=blog_id,
                body={
                    "title": title,
                    "content": html
                },
                isDraft=False
            ).execute()

            return {
                "status": "BLOGGER_LIVE",
                "post_id": post.get("id")
            }

        except Exception as e:
            return {
                "status": "BLOGGER_ERROR",
                "error": str(e)
            }

    # =========================
    # YOUTUBE UPLOAD (SAFE HOOK)
    # =========================
    def publish_youtube(self, video_path, title):

        if not self.LIVE_MODE:
            return {
                "status": "SIMULATED_YOUTUBE",
                "file": video_path
            }

        return {
            "status": "YOUTUBE_LIVE_READY",
            "note": "Upload hook ready - needs OAuth user token"
        }

    # =========================
    # PINTEREST QUEUE
    # =========================
    def publish_pinterest(self, title, description):

        return {
            "status": "PIN_QUEUED",
            "title": title,
            "description": description
        }

    # =========================
    # FULL DISTRIBUTION
    # =========================
    def distribute(self, product_bundle):

        results = []

        for item in product_bundle:

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
                    item.get("description", "")
                ),

                "timestamp": datetime.utcnow().isoformat(),
                "status": "DISTRIBUTED_SAFE"
            })

        return {
            "status": "LIVE_DISTRIBUTION_READY",
            "live_mode": self.LIVE_MODE,
            "results": results
        }
