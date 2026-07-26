class MailRouter:

    def __init__(self):

        self.rules = {
            "Amazon": [
                "amazon",
                "partnernet",
                "prime",
                "black friday",
                "cyber monday",
                "deal",
                "aktion",
                "werbemittel",
                "banner"
            ],

            "Tarifcheck": [
                "tarifcheck"
            ],

            "Check24": [
                "check24"
            ],

            "Telekom": [
                "telekom"
            ],

            "Congstar": [
                "congstar"
            ]
        }


    def analyze(self, mail):

        text = (
            mail.get("sender","") +
            " " +
            mail.get("subject","")
        ).lower()


        for partner, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:

                    return {
                        "status": "RELEVANT",
                        "partner": partner,
                        "reason": keyword
                    }


        return {
            "status": "IGNORE",
            "partner": "UNKNOWN",
            "reason": ""
        }
