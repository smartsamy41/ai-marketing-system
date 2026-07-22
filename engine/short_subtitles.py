class ShortSubtitleBuilder:


    def create(
        self,
        title,
        description,
        cta
    ):

        return [
            {
                "start":0,
                "end":3,
                "text":title
            },
            {
                "start":3,
                "end":15,
                "text":description
            },
            {
                "start":15,
                "end":25,
                "text":"Angebote und Informationen vergleichen"
            },
            {
                "start":25,
                "end":30,
                "text":cta
            }
        ]
