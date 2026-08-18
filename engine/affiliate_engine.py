from typing import Any

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


class AffiliateEngine:

    """
    Zentrale Affiliate Asset Steuerung.

    Eine zentrale Quelle für:
    - Produktdaten
    - Werbemittel
    - Tracking URLs
    - Affiliate URLs
    """


    def __init__(
        self,
        sheet_id: str | None = None,
        credentials_json: str | None = None
    ):

        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=(
                sheet_id
                or secrets.get("GOOGLE_SHEET_ID")
            ),
            credentials_json=(
                credentials_json
                or secrets.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            )
        )

        self.products = []
        self.assets = []

        self.reload()



    def reload(self):

        self.products = self.sheets.read_records(
            "products",
            "A:ZZ"
        )

        self.assets = self.sheets.read_records(
            "affiliate_assets_clean",
            "A:ZZ"
        )



    @staticmethod
    def clean(value):

        if value is None:
            return ""

        text = str(value).strip()

        if text.lower() in (
            "nan",
            "none",
            "null"
        ):
            return ""

        return text



    @staticmethod
    def normalize(value: Any):

        return AffiliateEngine.clean(
            value
        ).lower()



    def product_id(self, record):

        return self.clean(
            record.get("product_id")
            or record.get("produkt_id")
        )



    def find_product(
        self,
        product
    ):

        search = self.normalize(
            product
        )


        for record in self.products:

            ids = [
                self.normalize(
                    record.get("product_id")
                ),
                self.normalize(
                    record.get("produkt_id")
                ),
                self.normalize(
                    record.get("product_name")
                ),
                self.normalize(
                    record.get("name")
                )
            ]


            if search in ids:
                return record


        return None



    def find_assets(
        self,
        product_id
    ):

        result = []

        target = self.normalize(
            product_id
        )


        for asset in self.assets:

            asset_id = self.normalize(
                asset.get("product_id")
                or asset.get("produkt_id")
            )


            if asset_id == target:
                result.append(asset)


        return result



    def select_primary_asset(
        self,
        product_id
    ):

        assets = self.find_assets(
            product_id
        )


        if not assets:
            return None



        for asset in assets:

            html = self.clean(
                asset.get("html_code")
                or asset.get("html")
                or asset.get("vergleichsrechner_html")
                or asset.get("banner_300x250_html")
            )


            url = self.clean(
                asset.get("affiliate_url")
                or asset.get("direktlink")
                or asset.get("tracking_url")
            )


            if html or url:

                return {

                    "asset_type":
                        self.clean(
                            asset.get("werbemittel_typ")
                            or asset.get("asset_type")
                        ),

                    "html":
                        html,

                    "affiliate_url":
                        url,

                    "tracking_url":
                        url,

                    "cta":
                        self.clean(
                            asset.get("cta")
                        )
                        or
                        "Vergleich starten",

                    "kennzeichnung":
                        self.clean(
                            asset.get("kennzeichnung")
                        )
                        or
                        "Werbung / Anzeige"

                }


        return None



    def get_product_data(
        self,
        product
    ):

        record = self.find_product(
            product
        )


        if not record:

            return {
                "status": "NOT_FOUND"
            }



        product_id = self.product_id(
            record
        )


        primary_asset = self.select_primary_asset(
            product_id
        )


        tracking_url = self.clean(
            record.get("tracking_url")
        )


        if not tracking_url and primary_asset:

            tracking_url = self.clean(
                primary_asset.get(
                    "affiliate_url"
                )
            )



        return {

            "status":
                "FOUND",

            "product_id":
                product_id,

            "product_name":
                self.clean(
                    record.get("product_name")
                    or record.get("name")
                ),

            "partner":
                self.clean(
                    record.get("partner")
                ),

            "primary_asset":
                primary_asset,

            "tracking_url":
                tracking_url,

            "affiliate_url":
                tracking_url,

            "assets":
                self.find_assets(
                    product_id
                )
        }
