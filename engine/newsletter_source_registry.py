import json
from pathlib import Path


class NewsletterSourceRegistry:


    def __init__(self):

        self.base = Path(
            "data_master"
        )

        self.registry_file = (
            self.base
            / "newsletter_layer"
            / "newsletter_registry.json"
        )

        self.sources_file = (
            self.base
            / "source_layer"
            / "partner_sources.json"
        )

        self.registry = self.load(
            self.registry_file
        )

        self.partner_sources = self.load(
            self.sources_file
        )


    def load(self, path):

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def get_partners(self):

        return self.registry.get(
            "sources",
            []
        )



    def detect_partner(
        self,
        sender,
        subject=""
    ):

        text = (
            sender
            +
            " "
            +
            subject
        ).lower()


        rules = {

            "Amazon": [
                "associates@amazon.de",
                "store-news@amazon.com",
                "amazon influencer",
                "amazon associates"
            ],


            "Check24": [
                "check24.net",
                "check24-partnerprogramm.de"
            ],


            "Tarifcheck": [
                "tarifcheck-partnerprogramm.de"
            ],


            "Telekom Profis": [
                "telekom-profis.de"
            ]

        }


        for partner, patterns in rules.items():

            for pattern in patterns:

                if pattern in text:

                    return {
                        "status": "VERIFIED",
                        "partner": partner,
                        "source": pattern
                    }


        return {
            "status": "UNKNOWN",
            "partner": "",
            "source": ""
        }



    def validate(
        self,
        mail
    ):

        result = self.detect_partner(
            mail.get("sender",""),
            mail.get("subject","")
        )


        return result
