from typing import Any

from engine.google_sheets_live import GoogleSheetsLive


class AffiliateEngine:

    """
    Zentrale Affiliate Asset Steuerung.

    Regel:
    Ein Produkt = ein Primary Asset

    Ausgabe:
    product_id
    primary_asset
    cta
    tracking_url
    alt_text

    Datenquellen:
    1. products
    2. affiliate_assets_clean
    """


    def __init__(
        self,
        sheet_id: str | None = None,
        credentials_json: str | None = None
    ):

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=sheet_id,
            credentials_json=credentials_json
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
    def _normalize(
        value: Any
    ) -> str:

        return str(
            value or ""
        ).strip().lower()



    @staticmethod
    def _product_id(
        record
    ) -> str:

        return str(
            record.get("product_id")
            or record.get("produkt_id")
            or ""
        ).strip()



    def find_product(
        self,
        product
    ):

        search = self._normalize(
            product
        )

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



    def find_assets(
        self,
        product_id
    ):

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

                result.append(
                    asset
                )

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


        asset = assets[0]


        return {

            "asset_id":
                asset.get(
                    "asset_id",
                    ""
                ),

            "asset_type":
                asset.get(
                    "asset_type",
                    ""
                ),

            "html":
                asset.get(
                    "html"
                    or
                    "banner_html"
                    or
                    "vergleichsrechner_html"
                    or
                    ""
                ),

            "image_url":
                asset.get(
                    "image_url",
                    ""
                ),

            "alt_text":
                asset.get(
                    "alt_text"
                    or
                    f"Werbung für {product_id}"
                ),

            "cta":
                asset.get(
                    "cta"
                    or
                    "Vergleich starten"
                )

        }



    def get_tracking_link(
        self,
        product
    ):

        record = self.find_product(
            product
        )

        if not record:

            return None


        return str(

            record.get(
                "tracking_url_v3"
            )

            or

            record.get(
                "tracking_url"
            )

            or

            record.get(
                "affiliate_url"
            )

            or
            ""

        ).strip()



    def get_affiliate_link(
        self,
        product
    ):

        record = self.find_product(
            product
        )

        if not record:

            return None


        return str(

            record.get(
                "affiliate_url"
            )

            or

            record.get(
                "official_direct_link"
            )

            or

            record.get(
                "target_url"
            )

            or
            ""

        ).strip()



    def get_product_data(
        self,
        product
    ):

        record = self.find_product(
            product
        )


        if not record:

            return {

                "status":
                    "NOT_FOUND",

                "product":
                    product

            }



        product_id = self._product_id(
            record
        )


        primary_asset = self.select_primary_asset(
            product_id
        )


        return {


            "status":
                "FOUND",


            "product_id":
                product_id,


            "product_name":
                record.get(
                    "product_name"
                ),


            "source":
                record.get(
                    "source"
                ),


            "category":
                record.get(
                    "category"
                ),


            "primary_asset":
                primary_asset,


            "cta":
                (
                    primary_asset.get(
                        "cta"
                    )
                    if primary_asset
                    else
                    "Vergleich starten"
                ),


            "tracking_url":
                self.get_tracking_link(
                    product_id
                ),


            "affiliate_url":
                self.get_affiliate_link(
                    product_id
                )

        }



_default_engine = None



def get_affiliate_link(
    product
):

    global _default_engine


    if _default_engine is None:

        _default_engine = AffiliateEngine()



    return _default_engine.get_affiliate_link(
        product
    )
