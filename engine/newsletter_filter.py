from engine.newsletter_source_registry import NewsletterSourceRegistry


class NewsletterFilter:


    def __init__(self):

        self.source_registry = NewsletterSourceRegistry()


        self.categories = {

            "Amazon":
                "AMAZON_AFFILIATE",

            "Check24":
                "CHECK24_PARTNER",

            "Tarifcheck":
                "TARIFCHECK_PARTNER",

            "Telekom Profis":
                "TELEKOM_PARTNER"

        }


        self.ignore_rules = [

            "account-update@amazon.de",
            "sell.amazon.com",
            "business.amazon.de",
            "develop.amazon.com",
            "security",
            "passwort"

        ]



    def analyze(
        self,
        mail
    ):

        sender = mail.get(
            "sender",
            ""
        ).lower()


        subject = mail.get(
            "subject",
            ""
        ).lower()


        text = (
            sender
            +
            " "
            +
            subject
        )



        for rule in self.ignore_rules:

            if rule in text:

                return {

                    "status":
                        "IGNORE",

                    "partner":
                        "",

                    "category":
                        "IGNORE",

                    "keyword":
                        rule

                }



        source_result = self.source_registry.validate(
            mail
        )


        if source_result["status"] == "VERIFIED":


            partner = source_result["partner"]


            return {

                "status":
                    "KEEP",

                "partner":
                    partner,

                "category":
                    self.categories.get(
                        partner,
                        "PARTNER"
                    ),

                "keyword":
                    source_result["source"],

                "source":
                    source_result["source"]

            }



        return {

            "status":
                "IGNORE",

            "partner":
                "",

            "category":
                "UNKNOWN",

            "keyword":
                ""

        }
