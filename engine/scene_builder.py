class SceneBuilder:

    def build(
        self,
        title: str,
        description: str,
        cta: str
    ):

        return [
            {
                "duration": 3,
                "text": title
            },
            {
                "duration": 8,
                "text": "Vergleiche wichtige Informationen und finde passende Angebote."
            },
            {
                "duration": 10,
                "text": description
            },
            {
                "duration": 9,
                "text": cta
            }
        ]
