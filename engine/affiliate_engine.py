from typing import Any

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


class AffiliateEngine:

    """
    Zentrale Affiliate Asset Steuerung.

    Regel:
    Ein Produkt = ein Primary Asset
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
    def _normalize(value: Any) -> str:

        return str(
            value or ""
        ).strip().lower()


    @staticmethod
    def _product_id(record):

        return str(
            record.get("product_id")
            or record.get("produkt_id")
            or ""
        ).strip()


    def find_product(self, product):

        search = self._normalize(product)

        for record in self.products:

            if search in {

                self._normalize(
                    record.get("product_id")
                ),

                self._normalize(
                    record.get("product_name")
                )

            }:

                return record

        return None


    def find_assets(self, product_id):

        result = []

        target = self._normalize(
            product_id
        )

        for asset in self.assets:

            asset_id = self._normalize(
                asset.get("produkt_id")
                or asset.get("product_id")
            )

            if asset_id == target:

                result.append(asset)

        return result


    def select_primary_asset(self, product_id):

        assets = self.find_assets(
            product_id
        )

        if not assets:

            return None


        asset = assets[0]

        return {

            "asset_type":
                asset.get("werbemittel_typ")
                or asset.get("asset_type")
                or "",

            "html":
                asset.get("html_code")
                or asset.get("html")
                or asset.get("banner_300x250_html")
                or asset.get("vergleichsrechner_html")
                or "",

            "affiliate_url":
                asset.get("affiliate_url")
                or asset.get("direktlink")
                or "",

            "cta":
                asset.get("cta")
                or "Vergleich starten",

            "kennzeichnung":
                asset.get("kennzeichnung")
                or "Werbung / Anzeige"

        }


    def get_product_data(self, product):

        record = self.find_product(
            product
        )

        if not record:

            return {
                "status": "NOT_FOUND"
            }


        product_id = self._product_id(
            record
        )


        primary_asset = self.select_primary_asset(
            product_id
        )


        return {

            "status": "FOUND",

            "product_id": product_id,

            "product_name":
                record.get(
                    "product_name"
                ),

            "primary_asset":
                primary_asset,

            "tracking_url":
                record.get(
                    "tracking_url"
                    or ""
                )

        }
