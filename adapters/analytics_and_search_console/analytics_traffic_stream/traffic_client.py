from datetime import datetime, timezone


class TrafficStreamClient:

    def __init__(
        self,
        source="analytics"
    ):

        self.source = source


    def register_event(
        self,
        event_type,
        page_url,
        metadata=None
    ):

        return {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "source": self.source,

            "event_type": event_type,

            "page_url": page_url,

            "metadata": metadata or {},

            "status": "ready_for_learning"
        }


    def analyze_signal(
        self,
        signal
    ):

        return {
            "signal": signal,
            "status": "pending_analysis"
        }


if __name__ == "__main__":

    client = TrafficStreamClient()

    print(
        client.register_event(
            "page_view",
            "https://freebasics.online/"
        )
    )
