import json
from datetime import datetime, timezone
from pathlib import Path


class PartnerNewsletterAnalyzer:


    def __init__(self):

        base = Path("data_master")

        self.sources = self.load_json(
            base / "source_layer" / "partner_sources.json"
        )

        self.mapping = self.load_json(
            base / "newsletter_layer" / "newsletter_product_mapping.json"
        )

        self.keyword_mapping = self.load_json(
            base / "newsletter_layer" / "product_keyword_mapping.json"
        )

        self.catalog = self.load_json(
            base / "catalog" / "product_master_44.json"
        )



    def load_json(self, path):

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def detect_partner(self, mail):

        text = (
            mail.get("sender", "")
            + " "
            + mail.get("subject", "")
            + " "
            + mail.get("body_text", "")
        ).lower()


        rules = {

            "Amazon": [
                "amazon",
                "associates",
                "partnernet"
            ],

            "Telekom": [
                "telekom",
                "telekom-profis"
            ],

            "Check24": [
                "check24"
            ],

            "Tarifcheck": [
                "tarifcheck"
            ]

        }


        for partner, keywords in rules.items():

            for keyword in keywords:

                if keyword in text:

                    return partner


        return "UNKNOWN"



    def validate_source(self, partner, mail):

        sender = mail.get(
            "sender",
            ""
        ).lower()


        rules = {

            "Amazon": [
                "amazon"
            ],

            "Telekom": [
                "telekom"
            ],

            "Check24": [
                "check24"
            ],

            "Tarifcheck": [
                "tarifcheck"
            ]

        }


        for keyword in rules.get(
            partner,
            []
        ):

            if keyword in sender:

                return True


        return False



    def find_product(self, product_id):

        for product in self.catalog.get(
            "products",
            []
        ):

            if product.get(
                "product_id"
            ) == product_id:

                return product


        return None



    def match_products(self, partner, mail):

        text = (
            mail.get("subject", "")
            + " "
            + mail.get("body_text", "")
        ).lower()


        result = []


        keywords = self.keyword_mapping.get(
            "keywords",
            {}
        )


        for product_id, terms in keywords.items():

            product = self.find_product(
                product_id
            )


            if not product:

                continue


            if product.get(
                "partner",
                ""
            ).lower() != partner.lower():

                continue


            for term in terms:

                if term.lower() in text:

                    result.append(
                        {
                            "product_id": product.get(
                                "product_id"
                            ),

                            "name": product.get(
                                "name"
                            ),

                            "category": product.get(
                                "category"
                            ),

                            "keyword": term
                        }
                    )

                    break


        return result



    def get_content_types(self, partner):

        return self.mapping.get(
            "mapping",
            {}
        ).get(
            partner,
            {}
        ).get(
            "content_types",
            []
        )



    def analyze(self, mail):

        partner = self.detect_partner(
            mail
        )


        source_verified = self.validate_source(
            partner,
            mail
        )


        products = self.match_products(
            partner,
            mail
        )


        return {

            "email_id": mail.get(
                "message_id",
                ""
            ),

            "partner": partner,

            "source_verified": source_verified,

            "product_match": products,

            "content_types": self.get_content_types(
                partner
            ),

            "subject": mail.get(
                "subject",
                ""
            ),

            "status":
                "READY"
                if source_verified
                else "BLOCKED",

            "created_at": datetime.now(
                timezone.utc
            ).isoformat()

        }
