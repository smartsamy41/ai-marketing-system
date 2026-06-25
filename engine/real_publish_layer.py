import os


class RealPublishLayer:

    # =========================
    # BLOGGER PUBLISH (SAFE STRUCTURE)
    # =========================
    def publish_to_blogger(self, product_id, content):

        blog_id = os.getenv("BLOGGER_BLOG_ID")

        return {
            "platform": "blogger",
            "blog_id": blog_id,
            "product_id": product_id,
            "title": content.get("title"),
            "status": "READY_TO_PUBLISH",
            "action": "CREATE_POST"
        }

    # =========================
    # PINTEREST QUEUE
    # =========================
    def publish_to_pinterest(self, product_id, content):

        return {
            "platform": "pinterest",
            "product_id": product_id,
            "title": content.get("title"),
            "status": "QUEUED",
            "action": "CREATE_PIN"
        }

    # =========================
    # YOUTUBE OUTPUT (NO UPLOAD YET SAFE)
    # =========================
    def publish_to_youtube(self, product_id, content):

        return {
            "platform": "youtube",
            "product_id": product_id,
            "title": content.get("title"),
            "status": "SCRIPT_READY",
            "action": "VIDEO_SCRIPT_ONLY"
        }

    # =========================
    # MASTER PUBLISH FUNCTION
    # =========================
    def publish_all(self, product_id, content):

        return {
            "product_id": product_id,

            "blogger": self.publish_to_blogger(product_id, content),
            "pinterest": self.publish_to_pinterest(product_id, content),
            "youtube": self.publish_to_youtube(product_id, content),

            "status": "REAL_PUBLISH_LAYER_ACTIVE"
        }
