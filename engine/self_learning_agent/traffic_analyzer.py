class TrafficAnalyzer:

    def __init__(
        self,
        source="analytics"
    ):

        self.source = source


    def analyze(
        self,
        events
    ):

        result = {
            "source": self.source,
            "events_total": len(events),
            "signals": []
        }

        for event in events:

            result["signals"].append(
                {
                    "page": event.get("page"),
                    "event_type": event.get("event_type"),
                    "product_id": event.get("product_id")
                }
            )

        return result


    def detect_interest(
        self,
        events
    ):

        products = {}

        for event in events:

            product_id = event.get(
                "product_id"
            )

            if product_id:

                products[product_id] = (
                    products.get(product_id, 0) + 1
                )

        return products


if __name__ == "__main__":

    analyzer = TrafficAnalyzer()

    print(
        analyzer.analyze(
            [
                {
                    "page": "/lp/CHK24_001",
                    "event_type": "click",
                    "product_id": "CHK24_001"
                }
            ]
        )
    )
