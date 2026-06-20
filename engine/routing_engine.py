from datetime import datetime


def route_output(product):

    try:

        source = str(product.get("source") or "").lower()

        if "amazon" in source:
            channel = "landingpage"

        elif "check24" in source:
            channel = "landingpage"

        elif "tarifcheck" in source:
            channel = "landingpage"

        elif "telekom" in source:
            channel = "landingpage"

        else:
            channel = "default"

        return {
            "status": "ROUTING_OK",
            "channel": channel,
            "product_id": product.get("product_id"),
            "timestamp": str(datetime.now())
        }

    except Exception as e:

        return {
            "status": "ROUTING_FAILED",
            "error": str(e),
            "timestamp": str(datetime.now())
        }


class RoutingEngine:

    def __init__(self):
        print("🟢 RoutingEngine loaded")

    def route(self, product):
        return route_output(product)
