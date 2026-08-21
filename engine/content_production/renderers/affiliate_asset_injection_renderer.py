import json
from pathlib import Path
from datetime import datetime, timezone


class AffiliateAssetInjectionRenderer:

    def __init__(self):

        self.source = Path(
            "data_master/content_intelligence/"
            "affiliate_asset_knowledge_graph.json"
        )

        self.output = Path(
            "data_master/content_production/"
            "affiliate_asset_output"
        )


    # =========================================================
    # HELPERS
    # =========================================================

    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    @staticmethod
    def clean(value):

        if value is None:
            return None

        if isinstance(value, str):

            value = value.strip()

            if value.lower() in {
                "",
                "nan",
                "none",
                "null",
                "nicht verfügbar",
                "nicht verfuegbar"
            }:
                return None

        return value


    # =========================================================
    # PARTNER
    # =========================================================

    def detect_partner(
        self,
        product_id,
        asset
    ):

        partner = self.clean(
            asset.get("partner")
        )

        if partner:
            return str(partner).lower()

        pid = str(
            product_id or ""
        ).upper()

        if pid.startswith("CHK24_"):
            return "check24"

        if pid.startswith("TC_"):
            return "tarifcheck"

        if pid.startswith("TEL_"):
            return "telekom"

        return "amazon"


    # =========================================================
    # ASSET TYPE
    # =========================================================

    def detect_asset_type(
        self,
        asset
    ):

        explicit = self.clean(
            asset.get("asset_type")
        )

        if explicit:
            return explicit


        asset_id = str(
            asset.get("asset_id", "")
        ).upper()


        source = str(
            asset.get("source", "")
        ).lower()


        if "_ROUTING" in asset_id:
            return "verified_routing_link"


        if "_DIRECT" in asset_id:
            return "direct_link"


        if "_CALCULATOR" in asset_id:
            return "calculator"


        if "_SHORT" in asset_id:
            return "short_calculator"


        if "_BANNER_300" in asset_id:
            return "banner_300x250"


        if "_BANNER_728" in asset_id:
            return "banner_728x90"


        if "direktlink" in source:
            return "direct_link"


        if "vergleichsrechner" in source:
            return "calculator"


        if "kurzrechner" in source:
            return "short_calculator"


        if "300x250" in source:
            return "banner_300x250"


        if "728x90" in source:
            return "banner_728x90"


        return "affiliate_asset"


    # =========================================================
    # PAYLOAD
    # =========================================================

    def get_payload(
        self,
        asset
    ):

        #
        # V5 KNOWLEDGE GRAPH
        #
        # Primary field:
        # payload
        #

        payload = self.clean(
            asset.get("payload")
        )

        if payload:
            return payload


        #
        # Backward compatibility
        #

        fallback_fields = [

            "direct_link",

            "calculator",

            "short_calculator",

            "banner_300x250",

            "banner_728x90",

            "affiliate_url",

            "tracking_url",

            "html",

            "url",

            "image_url"

        ]


        for field in fallback_fields:

            value = self.clean(
                asset.get(field)
            )

            if value:
                return value


        return None


    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        data = self.load_json(
            self.source
        )


        assets = data.get(
            "assets",
            []
        )


        connections = data.get(
            "connections",
            {}
        )


        product_asset_links = connections.get(
            "product_to_asset",
            []
        )


        tracking_links = connections.get(
            "asset_to_tracking",
            []
        )


        compliance_links = connections.get(
            "asset_to_compliance",
            []
        )


        partner_rules = data.get(
            "partner_rules",
            []
        )


        # =====================================================
        # ASSET LOOKUP
        # =====================================================

        asset_lookup = {}


        for asset in assets:

            asset_id = self.clean(
                asset.get("asset_id")
            )

            if asset_id:

                asset_lookup[
                    asset_id
                ] = asset


        # =====================================================
        # PRODUCT GRAPH
        # =====================================================

        products = {}


        missing_asset_ids = []


        duplicate_links_removed = 0


        for link in product_asset_links:

            product_id = self.clean(
                link.get("product_id")
            )


            if not product_id:
                continue


            products.setdefault(
                product_id,
                []
            )


            asset_ids = link.get(
                "assets",
                []
            )


            #
            # Legacy compatibility
            #

            if not asset_ids:

                legacy_id = self.clean(
                    link.get("asset_id")
                )

                if legacy_id:

                    asset_ids = [
                        legacy_id
                    ]


            seen = set()


            for asset_id in asset_ids:

                asset_id = self.clean(
                    asset_id
                )


                if not asset_id:
                    continue


                if asset_id in seen:

                    duplicate_links_removed += 1

                    continue


                seen.add(
                    asset_id
                )


                asset = asset_lookup.get(
                    asset_id
                )


                if not asset:

                    missing_asset_ids.append(

                        {
                            "product_id":
                                product_id,

                            "asset_id":
                                asset_id
                        }

                    )

                    continue


                partner = self.detect_partner(
                    product_id,
                    asset
                )


                asset_type = self.detect_asset_type(
                    asset
                )


                payload = self.get_payload(
                    asset
                )


                compliance = (
                    asset.get(
                        "compliance",
                        {}
                    )
                    or {}
                )


                tracking = self.clean(
                    asset.get("tracking")
                )


                source_verified = bool(

                    asset.get(
                        "official_data_only"
                    )

                    or

                    asset.get(
                        "source_verified"
                    )

                    or

                    str(
                        asset.get(
                            "status",
                            ""
                        )
                    ).lower()
                    in {
                        "offiziell geliefert",
                        "verified_source",
                        "verified_product_routing",
                        "official",
                        "verified"
                    }

                )


                product_asset = {

                    "asset_id":
                        asset_id,


                    "product_id":
                        product_id,


                    "product_name":
                        self.clean(
                            asset.get(
                                "product_name"
                            )
                        ),


                    "partner":
                        partner,


                    "asset_type":
                        asset_type,


                    "source":
                        self.clean(
                            asset.get(
                                "source"
                            )
                        ),


                    "format":
                        self.clean(
                            asset.get(
                                "format"
                            )
                        ),


                    "status":
                        self.clean(
                            asset.get(
                                "status"
                            )
                        ),


                    "payload":
                        payload,


                    "payload_available":
                        bool(
                            payload
                        ),


                    "tracking":
                        tracking,


                    "tracking_required":
                        True,


                    "advertising_label_required":
                        True,


                    "official_asset_required":
                        True,


                    "source_verified":
                        source_verified,


                    "fabricated":
                        False,


                    "compliance":
                        compliance

                }


                products[
                    product_id
                ].append(
                    product_asset
                )


        # =====================================================
        # FINAL DEDUPLICATION
        # =====================================================

        for product_id in list(
            products.keys()
        ):

            unique = {}

            clean_assets = []


            for asset in products[
                product_id
            ]:

                asset_id = asset.get(
                    "asset_id"
                )


                if asset_id in unique:

                    duplicate_links_removed += 1

                    continue


                unique[
                    asset_id
                ] = True


                clean_assets.append(
                    asset
                )


            products[
                product_id
            ] = clean_assets


        # =====================================================
        # AUDIT
        # =====================================================

        total_product_assets = 0

        payload_ready = 0

        payload_missing = 0

        source_verified = 0


        partner_stats = {}


        for product_id, product_assets in (
            products.items()
        ):

            for asset in product_assets:

                total_product_assets += 1


                if asset.get(
                    "payload_available"
                ):

                    payload_ready += 1

                else:

                    payload_missing += 1


                if asset.get(
                    "source_verified"
                ):

                    source_verified += 1


                partner = asset.get(
                    "partner",
                    "unknown"
                )


                partner_stats.setdefault(

                    partner,

                    {
                        "assets": 0,
                        "payload_ready": 0,
                        "payload_missing": 0
                    }

                )


                partner_stats[
                    partner
                ][
                    "assets"
                ] += 1


                if asset.get(
                    "payload_available"
                ):

                    partner_stats[
                        partner
                    ][
                        "payload_ready"
                    ] += 1

                else:

                    partner_stats[
                        partner
                    ][
                        "payload_missing"
                    ] += 1


        products_without_assets = [

            product_id

            for product_id, product_assets
            in products.items()

            if not product_assets

        ]


        # =====================================================
        # RESULT
        # =====================================================

        result = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "affiliate_asset_injection",


            "version":
                "4.0",


            "created":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "status":
                "ACTIVE",


            "rules": {

                "official_assets_only":
                    True,

                "no_fabricated_assets":
                    True,

                "tracking_required":
                    True,

                "advertising_disclosure_required":
                    True,

                "missing_payload_must_not_be_invented":
                    True,

                "partner_compliance_required":
                    True

            },


            "products":
                products,


            "partner_rules":
                partner_rules,


            "connections": {

                "product_to_asset":
                    product_asset_links,

                "asset_to_tracking":
                    tracking_links,

                "asset_to_compliance":
                    compliance_links

            },


            "audit": {

                "source_assets":
                    len(
                        assets
                    ),

                "products":
                    len(
                        products
                    ),

                "total_product_assets":
                    total_product_assets,

                "payload_ready":
                    payload_ready,

                "payload_missing":
                    payload_missing,

                "source_verified":
                    source_verified,

                "duplicate_links_removed":
                    duplicate_links_removed,

                "missing_asset_ids":
                    missing_asset_ids,

                "missing_asset_id_count":
                    len(
                        missing_asset_ids
                    ),

                "products_without_assets":
                    products_without_assets,

                "products_without_assets_count":
                    len(
                        products_without_assets
                    ),

                "partner_stats":
                    partner_stats

            }

        }


        # =====================================================
        # WRITE
        # =====================================================

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        file = (

            self.output
            /
            "affiliate_asset_injection_graph.json"

        )


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=2,
                ensure_ascii=False
            )


        print(
            "AFFILIATE ASSET INJECTION GRAPH CREATED V4"
        )


        print(
            "PRODUCTS:",
            len(
                products
            )
        )


        print(
            "SOURCE ASSETS:",
            len(
                assets
            )
        )


        print(
            "PAYLOAD READY:",
            payload_ready
        )


        print(
            "PAYLOAD MISSING:",
            payload_missing
        )


        print(
            "DUPLICATE LINKS REMOVED:",
            duplicate_links_removed
        )


        print(
            "MISSING ASSET IDS:",
            len(
                missing_asset_ids
            )
        )


        print(
            "PRODUCTS WITHOUT ASSETS:",
            len(
                products_without_assets
            )
        )


        print(
            "PARTNERS:"
        )


        for partner, stats in (
            partner_stats.items()
        ):

            print(
                partner,
                stats
            )


if __name__ == "__main__":

    AffiliateAssetInjectionRenderer().build()
