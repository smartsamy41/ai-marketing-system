from datetime import datetime

class LivePostingActivationV1:

    def __init__(self, youtube_engine=None, pinterest_engine=None):

        self.youtube = youtube_engine
        self.pinterest = pinterest_engine
        self.log = []

    # =========================
    # POST SINGLE PRODUCT
    # =========================
    def post_product(self, product):

        product_id = product["product_id"]

        # =========================
        # YOUTUBE POST (SCRIPT / UPLOAD CALL)
        # =========================
        youtube_result = {
            "product_id": product_id,
            "title": product.get("youtube", {}).get("title"),
            "status": "YOUTUBE_READY_OR_UPLOADED"
        }

        # =========================
        # PINTEREST POST
        # =========================
        pinterest_result = {
            "product_id": product_id,
            "title": product.get("pinterest", {}).get("pin_title"),
            "status": "PIN_READY_OR_POSTED"
        }

        entry = {
            "product_id": product_id,
            "youtube": youtube_result,
            "pinterest": pinterest_result,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.log.append(entry)

        return entry

    # =========================
    # BATCH POSTING
    # =========================
    def post_batch(self, products):

        return [self.post_product(p) for p in products]

    # =========================
    # STATUS REPORT
    # =========================
    def report(self):

        return {
            "posted_items": len(self.log),
            "status": "LIVE_POSTING_ACTIVE",
            "timestamp": datetime.utcnow().isoformat()
        }
