class AutoArticleIdeator:

    def __init__(
        self,
        source="learning_signals"
    ):

        self.source = source


    def create_ideas(
        self,
        signals
    ):

        ideas = []

        for signal in signals:

            ideas.append(
                {
                    "topic": signal.get("keyword"),
                    "product_id": signal.get("product_id"),
                    "reason": "traffic_interest",
                    "status": "idea_created"
                }
            )

        return {
            "source": self.source,
            "ideas": ideas,
            "count": len(ideas)
        }


    def prioritize(
        self,
        ideas
    ):

        return sorted(
            ideas,
            key=lambda x: x.get(
                "priority",
                0
            ),
            reverse=True
        )


if __name__ == "__main__":

    engine = AutoArticleIdeator()

    print(
        engine.create_ideas(
            [
                {
                    "keyword": "DSL",
                    "product_id": "CHK24_004"
                }
            ]
        )
    )
