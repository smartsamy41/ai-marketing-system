class RoutingEngine:

    def __init__(self):
        print("🟢 RoutingEngine loaded")

    def route(self, product):

        return {
            "platform": "blog",
            "target": product.get("source", "default")
        }
