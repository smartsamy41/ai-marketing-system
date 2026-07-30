from email.header import decode_header


class NewsletterMailRouter:

    def decode(self, value):

        if not value:
            return ""

        result = ""

        for part, encoding in decode_header(value):

            if isinstance(part, bytes):

                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )

            else:
                result += part

        return result


    def __init__(self):

        self.rules = {

            "Amazon_Partner": [
                "ads.amazon.com",
                "associates@amazon.de",
                "amazon associates",
                "amazon partnernet",
                "partnernet.amazon"
            ],


            "Free Basics/Partner/Check24": [
                "check24-partnerprogramm",
                "check24.net",
                "check24"
            ],


            "Free Basics/Partner/Tarifcheck": [
                "tarifcheck-partnerprogramm",
                "tarifcheck.de",
                "tarifcheck"
            ],


            "Free Basics/Partner/Telekom": [
                "telekom-profis.de",
                "telekom profis"
            ]

        }


    def route(self, mail):

        sender = self.decode(
            mail.get("sender", "")
        ).lower()

        subject = self.decode(
            mail.get("subject", "")
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
