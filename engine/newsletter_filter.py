class NewsletterFilter:

    def __init__(self):

        self.partner_rules = {

            "Amazon": {
                "keywords": [
                    "associates@amazon.de",
                    "amazon partnernet",
                    "partnernet",
                    "werbemittel",
                    "kampagne",
                    "aktion",
                    "ressourcen"
                ],
                "category": "AMAZON_AFFILIATE"
            },

            "Tarifcheck": {
                "keywords": [
                    "tarifcheck",
                    "partnerprogramm"
                ],
                "category": "TARIFCHECK_PARTNER"
            },

            "Check24": {
                "keywords": [
                    "check24"
                ],
                "category": "CHECK24_PARTNER"
            },

            "Telekom": {
                "keywords": [
                    "telekom",
                    "telekom-profis"
                ],
                "category": "TELEKOM_PARTNER"
            }
        }


        self.ignore_rules = [
            "account-update@amazon.de",
            "sell.amazon.com",
            "business.amazon.de",
            "develop.amazon.com",
            "security",
            "passwort"
        ]


    def analyze(self, mail):

        sender = mail.get(
            "sender",
            ""
        ).lower()

        subject = mail.get(
            "subject",
            ""
        ).lower()

        text = sender + " " + subject


        for rule in self.ignore_rules:

            if rule in text:

                return {
                    "status": "IGNORE",
                    "partner": "",
                    "category": "IGNORE",
                    "keyword": rule
                }


        for partner, data in self.partner_rules.items():

            for keyword in data["keywords"]:

                if keyword in text:

                    return {
                        "status": "KEEP",
                        "partner": partner,
                        "category": data["category"],
                        "keyword": keyword
                    }


        return {
            "status": "IGNORE",
            "partner": "",
            "category": "UNKNOWN",
            "keyword": ""
        }
