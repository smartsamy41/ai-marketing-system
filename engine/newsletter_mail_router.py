class NewsletterMailRouter:

    def __init__(self):

        self.rules = {

            "Amazon_Partner": [
                "associates@amazon.de",
                "amazon associates",
                "amazon partnernet"
            ],

            "Amazon_Newsletter": [
                "prime",
                "prime day",
                "kindle",
                "echo",
                "alexa",
                "fire tv",
                "smartphone",
                "launch",
                "deal"
            ],

            "Partner_Newsletter": [
                "tarifcheck",
                "check24",
                "telekom",
                "telekom-profis"
            ]

        }


    def route(self, mail):

        sender = mail.get(
            "sender",
            ""
        ).lower()

        subject = mail.get(
            "subject",
            ""
        ).lower()

        text = sender + " " + subject


        for folder, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:

                    return {
                        "status": "MOVE",
                        "folder": folder,
                        "keyword": keyword
                    }


        return {
            "status": "IGNORE",
            "folder": "",
            "keyword": ""
        }
