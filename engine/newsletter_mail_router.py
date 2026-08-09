from email.header import decode_header

from engine.newsletter_source_registry import NewsletterSourceRegistry


class NewsletterMailRouter:


    def __init__(self):

        self.registry = NewsletterSourceRegistry()


        self.routes = {

            "Amazon":
                "Amazon_Partner",

            "Check24":
                "Free Basics/Partner/Check24",

            "Tarifcheck":
                "Free Basics/Partner/Tarifcheck",

            "Telekom Profis":
                "Free Basics/Partner/Telekom"

        }



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



    def route(self, mail):


        validation = self.registry.validate(
            mail
        )


        if validation["status"] != "VERIFIED":

            return {

                "status":
                    "IGNORE",

                "folder":
                    "",

                "keyword":
                    ""

            }


        partner = validation["partner"]


        folder = self.routes.get(
            partner,
            ""
        )


        if not folder:

            return {

                "status":
                    "IGNORE",

                "folder":
                    "",

                "keyword":
                    ""

            }


        return {

            "status":
                "MOVE",

            "folder":
                folder,

            "keyword":
                validation["source"]

        }
