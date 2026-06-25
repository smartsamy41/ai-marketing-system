class TrackingEngine:

    def track(self, product_id):

        return {
            "product_id": product_id,
            "status": "TRACKED",
            "clicks": 0,
            "impressions": 0
        }


tracking = TrackingEngine()
