from typing import Any

from engine.google_sheets_live import GoogleSheetsLive


class AffiliateEngine:

    """
    Affiliate-Link-Zugriff über die bestehende
    Google-Sheets-Masterdatenbank.

    Priorität:
    1. products
    2. affiliate_assets_clean

    Es werden keine Platzhalterlinks erzeugt.
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

        self.products: list[dict[str, Any]] = []
        self.assets: list[dict[str, Any]] = []

        self.reload()


    # ========================================================
    # MASTER DATA LOAD
    # ========================================================

    def reload(self) -> None:

        self.products = self.sheets.read_records(
            "products",
            "A:ZZ"
        )

        self.assets = self.sheets.read_records(
            "affiliate_assets_clean",
            "A:ZZ"
        )


    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize(value: Any) -> str:

        return str(
            value or ""
        ).strip().lower()


    @staticmethod
    def _product_id(record: dict[str, Any]) -> str:

        return str(
            record.get("product_id")
            or record.get("produkt_id")
            or ""
        ).strip()


    # ========================================================
    # PRODUCT LOOKUP
    # ========================================================

    def find_product(
        self,
        product: str
    ) -> dict[str, Any] | None:

        search_value = self._normalize(
            product
        )

        if not search_value:
            return None

        for record in self.products:

            product_id = self._normalize(
                record.get("product_id")
            )

            product_name = self._normalize(
                record.get("product_name")
            )

            if search_value in {
                product_id,
                product_name
            }:
                return record

        return None


    # ========================================================
    # ASSET LOOKUP
    # ========================================================

    def find_assets(
        self,
        product_id: str
    ) -> list[dict[str, Any]]:

        normalized_id = self._normalize(
            product_id
        )

        results = []

        for record in self.assets:

            asset_product_id = self._normalize(
                record.get("produkt_id")
                or record.get("product_id")
            )

            if asset_product_id == normalized_id:
                results.append(record)

        return results


    # ========================================================
    # AFFILIATE LINK
    # ========================================================

    def get_affiliate_link(
        self,
        product: str
    ) -> str | None:

        record = self.find_product(
            product
        )

        if not record:
            return None

        source = self._normalize(
            record.get("source")
        )

        affiliate_url = str(
            record.get("affiliate_url")
            or record.get("official_direct_link")
            or record.get("target_url")
            or ""
        ).strip()

        if source == "telekom":

            return affiliate_url or (
                "https://free-basics.telekom-profis.de"
            )

        if affiliate_url:
            return affiliate_url

        product_id = self._product_id(
            record
        )

        for asset in self.find_assets(
            product_id
        ):

            asset_url = str(
                asset.get("affiliate_url")
                or asset.get("direktlink")
                or ""
            ).strip()

            if (
                asset_url
                and asset_url.lower()
                not in {
                    "nan",
                    "nicht verfügbar"
                }
            ):
                return asset_url

        return None


    # ========================================================
    # TRACKING LINK
    # ========================================================

    def get_tracking_link(
        self,
        product: str
    ) -> str | None:

        record = self.find_product(
            product
        )

        if not record:
            return None

        source = self._normalize(
            record.get("source")
        )

        if source == "telekom":

            return self.get_affiliate_link(
                product
            )

        tracking_url = str(
            record.get("tracking_url_v3")
            or record.get("tracking_url")
            or ""
        ).strip()

        if tracking_url:

            return tracking_url.replace(
                "europe-west3.run.app",
                "europe-west1.run.app"
            )

        return self.get_affiliate_link(
            product
        )


    # ========================================================
    # COMPLETE PRODUCT DATA
    # ========================================================

    def get_product_data(
        self,
        product: str
    ) -> dict[str, Any]:

        record = self.find_product(
            product
        )

        if not record:

            return {
                "status": "NOT_FOUND",
                "product": product
            }

        product_id = self._product_id(
            record
        )

        return {
            "status": "FOUND",
            "product_id": product_id,
            "product_name": record.get(
                "product_name"
            ),
            "source": record.get(
                "source"
            ),
            "category": record.get(
                "category"
            ),
            "affiliate_url": self.get_affiliate_link(
                product_id
            ),
            "tracking_url": self.get_tracking_link(
                product_id
            ),
            "landingpage_url": record.get(
                "landingpage_url"
            ),
            "final_url": record.get(
                "final_url"
            ),
            "image_url": record.get(
                "image_url"
            ),
            "assets": self.find_assets(
                product_id
            )
        }


# ============================================================
# COMPATIBILITY FUNCTION
# Bestehende Funktionssignatur bleibt nutzbar.
# ============================================================

_default_engine: AffiliateEngine | None = None


def get_affiliate_link(
    product: str
) -> str | None:

    global _default_engine

    if _default_engine is None:
        _default_engine = AffiliateEngine()

    return _default_engine.get_affiliate_link(
        product
    )
