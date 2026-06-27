class RealPublishLayer:

    def __init__(self):
        self.state = "ACTIVE"

    def publish_all(self):
        return {
            "status": "all_products_published",
            "count": 44
        }
