import json
import os


class ContentEngine:

    def __init__(self):
        self.base_path = "engine/content_assets"

    # =========================
    # LOAD CONTENT ASSET
    # =========================
    def load(self, product_id):

        path = os.path.join(self.base_path, f"{product_id.lower()}.json")

        if not os.path.exists(path):
            return {
                "status": "ERROR",
                "message": "CONTENT_NOT_FOUND",
                "product_id": product_id
            }

        with open(path, "r") as f:
            data = json.load(f)

        return {
            "status": "OK",
            "data": data
        }

    # =========================
    # TRANSFORM FOR ENGINE
    # =========================
    def transform(self, product_id):

        content = self.load(product_id)

        if content.get("status") != "OK":
            return content

        data = content["data"]

        return {
            "product_id": product_id,
            "title": data.get("title"),
            "headline": data.get("headline"),
            "seo": data.get("seo"),
            "cta": data.get("cta"),
            "channels": data.get("channels")
        }
