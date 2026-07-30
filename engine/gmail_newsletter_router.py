class GmailNewsletterRouter:

    def __init__(self):

        self.rules = {

            "Free Basics/Partner/Amazon": [
                "amazon",
                "amazon associates",
                "associates@amazon.de",
                "amazon ads",
                "partnernet"
            ],

            "Free Basics/Partner/Check24": [
                "check24",
                "check24-partnerprogramm"
            ],

            "Free Basics/Partner/Tarifcheck": [
                "tarifcheck",
                "tarifcheck-partnerprogramm"
            ],

            "Free Basics/Partner/Telekom": [
                "telekom-profis",
                "telekom"
            ]
        }


    def route(self, mail):

        sender = mail.get("sender","").lower()
        subject = mail.get("subject","").lower()

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
