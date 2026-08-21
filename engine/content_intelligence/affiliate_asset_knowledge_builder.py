import json
import csv
from pathlib import Path
from datetime import datetime, timezone

from engine.affiliate_engine import AffiliateEngine


class AffiliateAssetKnowledgeBuilder:

    def __init__(self):

        self.product_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.rules_csv = Path(
            "system_scan/FINAL_COMPLETE_SCAN/sheets/affiliate_rules_FULL.csv"
        )

        self.output = Path(
            "data_master/content_intelligence/"
            "affiliate_asset_knowledge_graph.json"
        )

        self.affiliate = AffiliateEngine()


    # =========================================================
    # CLEANING
    # =========================================================

    @staticmethod
    def clean(value):

        if value is None:
            return None

        text = str(value).strip()

        if text.lower() in {
            "",
            "nan",
            "none",
            "null",
            "nicht verfügbar",
            "nicht verfuegbar"
        }:
            return None

        return text


    # =========================================================
    # FILE HELPERS
    # =========================================================

    def read_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def read_csv(self, path):

        rows = []

        if not path.exists():
            return rows

        with open(
            path,
            encoding="utf-8-sig",
            newline=""
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:
                rows.append(row)

        return rows


    # =========================================================
    # PRODUCT HELPERS
    # =========================================================

    def get_product_id(self, row):

        return self.clean(
            row.get("produkt_id")
            or row.get("product_id")
        )


    def get_product_name(self, row):

        return self.clean(
            row.get("produkt_name")
            or row.get("product_name")
            or row.get("name")
        )


    def detect_partner(
        self,
        product_id,
        explicit_partner=None
    ):

        partner = self.clean(
            explicit_partner
        )

        if partner:
            return partner.lower()

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
    # ASSET CREATION
    # =========================================================

    def add_asset(
        self,
        graph,
        product_id,
        product_name,
        partner,
        asset_id,
        asset_type,
        payload,
        row=None
    ):

        row = row or {}

        payload = self.clean(
            payload
        )

        if not payload:
            return False


        compliance = {

            "kennzeichnung":
                self.clean(
                    row.get("kennzeichnung")
                ),

            "impressum":
                self.clean(
                    row.get("impressum_hinweis")
                ),

            "newsletter_regeln":
                self.clean(
                    row.get("newsletter_regeln")
                ),

            "verbote":
                self.clean(
                    row.get("verbote")
                )
        }


        tracking = self.clean(
            row.get("tracking_hinweis")
        )


        asset = {

            "asset_id":
                asset_id,

            "product_id":
                product_id,

            "product_name":
                product_name,

            "partner":
                partner,

            "asset_type":
                asset_type,

            "source":
                self.clean(
                    row.get("werbemittel_typ")
                    or row.get("source")
                    or asset_type
                ),

            "format":
                self.clean(
                    row.get("format")
                ),

            "status":
                self.clean(
                    row.get("status")
                )
                or "verified_source",

            "payload":
                payload,

            "tracking":
                tracking,

            "compliance":
                compliance,

            "official_data_only":
                True,

            "fabricated":
                False
        }


        graph["assets"].append(
            asset
        )


        graph[
            "connections"
        ][
            "asset_to_tracking"
        ].append(

            {
                "asset_id":
                    asset_id,

                "tracking":
                    tracking
            }

        )


        graph[
            "connections"
        ][
            "asset_to_compliance"
        ].append(

            {
                "asset_id":
                    asset_id,

                "compliance":
                    compliance
            }

        )


        return True


    # =========================================================
    # SHEET ASSET PROCESSING
    # =========================================================

    def process_sheet_asset(
        self,
        graph,
        row
    ):

        product_id = self.get_product_id(
            row
        )

        if not product_id:
            return


        product_name = self.get_product_name(
            row
        )


        product_record = self.affiliate.find_product(
            product_id
        ) or {}


        partner = self.detect_partner(

            product_id,

            product_record.get(
                "partner"
            )

        )


        created_ids = []


        asset_map = [

            (
                "DIRECT",
                "direct_link",
                row.get("direktlink")
                or row.get("affiliate_url")
            ),

            (
                "CALCULATOR",
                "calculator",
                row.get(
                    "vergleichsrechner_html"
                )
            ),

            (
                "SHORT",
                "short_calculator",
                row.get(
                    "kurzrechner_html"
                )
            ),

            (
                "BANNER_300",
                "banner_300x250",
                row.get(
                    "banner_300x250_html"
                )
            ),

            (
                "BANNER_728",
                "banner_728x90",
                row.get(
                    "banner_728x90_html"
                )
            )

        ]


        for (
            suffix,
            asset_type,
            payload
        ) in asset_map:


            payload = self.clean(
                payload
            )


            if not payload:
                continue


            asset_id = (
                f"{product_id}_{suffix}"
            )


            created = self.add_asset(

                graph=graph,

                product_id=product_id,

                product_name=product_name,

                partner=partner,

                asset_id=asset_id,

                asset_type=asset_type,

                payload=payload,

                row=row

            )


            if created:
                created_ids.append(
                    asset_id
                )


        return created_ids


    # =========================================================
    # ROUTING FALLBACK
    # =========================================================

    def create_verified_routing_asset(
        self,
        graph,
        product
    ):

        product_id = self.get_product_id(
            product
        )

        if not product_id:
            return None


        partner = self.detect_partner(

            product_id,

            product.get(
                "partner"
            )

        )


        data = self.affiliate.get_product_data(
            product_id
        )


        if data.get(
            "status"
        ) != "FOUND":

            return None


        affiliate_url = self.clean(

            data.get(
                "affiliate_url"
            )

            or

            data.get(
                "target_url"
            )

            or

            data.get(
                "tracking_url"
            )

        )


        if not affiliate_url:
            return None


        product_name = (

            self.clean(
                data.get(
                    "product_name"
                )
            )

            or

            self.get_product_name(
                product
            )

        )


        asset_id = (
            f"{product_id}_ROUTING"
        )


        created = self.add_asset(

            graph=graph,

            product_id=product_id,

            product_name=product_name,

            partner=partner,

            asset_id=asset_id,

            asset_type="verified_routing_link",

            payload=affiliate_url,

            row={
                "status":
                    "verified_product_routing",

                "werbemittel_typ":
                    "Verified Routing Link",

                "tracking_hinweis":
                    "Tracking über FREE BASICS "
                    "Affiliate Routing Engine."
            }

        )


        if created:
            return asset_id

        return None


    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        product_entities = self.read_json(
            self.product_file
        )


        rules = self.read_csv(
            self.rules_csv
        )


        live_assets = (
            self.affiliate.assets
            or []
        )


        live_products = (
            self.affiliate.products
            or []
        )


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "affiliate_asset_knowledge_graph",

            "version":
                "5.0",

            "created":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "status":
                "ACTIVE",

            "rules": {

                "official_data_only":
                    True,

                "no_fabricated_assets":
                    True,

                "tracking_required":
                    True,

                "compliance_required":
                    True,

                "nan_is_missing":
                    True,

                "live_sheet_preferred":
                    True,

                "verified_routing_fallback":
                    True
            },

            "partners":
                [],

            "products":
                [],

            "assets":
                [],

            "partner_rules":
                [],

            "connections": {

                "product_to_asset":
                    [],

                "asset_to_tracking":
                    [],

                "asset_to_compliance":
                    [],

                "partner_to_rule":
                    []
            },

            "audit": {}
        }


        # =====================================================
        # CANONICAL PRODUCT LIST
        # =====================================================

        canonical_products = {}


        for p in product_entities.get(
            "entities",
            []
        ):

            product_id = self.get_product_id(
                p
            )

            if not product_id:
                continue

            canonical_products[
                product_id
            ] = {

                "product_id":
                    product_id,

                "name":
                    self.get_product_name(
                        p
                    ),

                "partner":
                    self.detect_partner(
                        product_id,
                        p.get("partner")
                    )
            }


        for p in live_products:

            product_id = self.get_product_id(
                p
            )

            if not product_id:
                continue


            if product_id not in canonical_products:

                canonical_products[
                    product_id
                ] = {

                    "product_id":
                        product_id,

                    "name":
                        self.get_product_name(
                            p
                        ),

                    "partner":
                        self.detect_partner(
                            product_id,
                            p.get("partner")
                        )
                }


        graph["products"] = list(
            canonical_products.values()
        )


        graph["partners"] = sorted(

            {

                p.get("partner")

                for p in graph[
                    "products"
                ]

                if p.get(
                    "partner"
                )

            }

        )


        # =====================================================
        # LIVE AFFILIATE ASSETS
        # =====================================================

        product_asset_map = {

            product_id: []

            for product_id in canonical_products

        }


        for row in live_assets:

            product_id = self.get_product_id(
                row
            )

            if not product_id:
                continue


            created_ids = (
                self.process_sheet_asset(
                    graph,
                    row
                )
                or []
            )


            product_asset_map.setdefault(
                product_id,
                []
            )


            product_asset_map[
                product_id
            ].extend(
                created_ids
            )


        # =====================================================
        # DEDUPLICATE ASSETS
        # =====================================================

        unique_assets = {}

        for asset in graph["assets"]:

            asset_id = asset.get(
                "asset_id"
            )

            if asset_id:

                unique_assets[
                    asset_id
                ] = asset


        graph["assets"] = list(
            unique_assets.values()
        )


        # =====================================================
        # VERIFIED ROUTING FALLBACK
        # Amazon / Telekom / products without asset rows
        # =====================================================

        routing_assets_created = 0


        for product_id, product in (
            canonical_products.items()
        ):

            existing = list(

                dict.fromkeys(

                    product_asset_map.get(
                        product_id,
                        []
                    )

                )

            )


            if not existing:

                routing_id = (
                    self.create_verified_routing_asset(
                        graph,
                        product
                    )
                )


                if routing_id:

                    existing.append(
                        routing_id
                    )

                    routing_assets_created += 1


            product_asset_map[
                product_id
            ] = existing


        # Re-dedupe after routing assets

        unique_assets = {}

        for asset in graph["assets"]:

            asset_id = asset.get(
                "asset_id"
            )

            if asset_id:

                unique_assets[
                    asset_id
                ] = asset


        graph["assets"] = list(
            unique_assets.values()
        )


        # =====================================================
        # PRODUCT → ASSET CONNECTIONS
        # =====================================================

        for product_id in canonical_products:

            graph[
                "connections"
            ][
                "product_to_asset"
            ].append(

                {
                    "product_id":
                        product_id,

                    "assets":
                        list(
                            dict.fromkeys(
                                product_asset_map.get(
                                    product_id,
                                    []
                                )
                            )
                        )
                }

            )


        # =====================================================
        # PARTNER RULES
        # =====================================================

        for rule in rules:

            graph[
                "partner_rules"
            ].append(
                rule
            )


            graph[
                "connections"
            ][
                "partner_to_rule"
            ].append(

                {
                    "partner":
                        self.clean(
                            rule.get(
                                "partner"
                            )
                        ),

                    "rule_id":
                        self.clean(
                            rule.get(
                                "rule_id"
                            )
                        )
                }

            )


        # =====================================================
        # AUDIT
        # =====================================================

        products_without_assets = []


        for product_id in canonical_products:

            if not product_asset_map.get(
                product_id
            ):

                products_without_assets.append(
                    product_id
                )


        graph["audit"] = {

            "products":
                len(
                    canonical_products
                ),

            "live_asset_rows":
                len(
                    live_assets
                ),

            "generated_assets":
                len(
                    graph["assets"]
                ),

            "routing_assets_created":
                routing_assets_created,

            "products_without_assets":
                products_without_assets,

            "products_without_assets_count":
                len(
                    products_without_assets
                ),

            "fabricated_assets":
                0
        }


        # =====================================================
        # WRITE
        # =====================================================

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                graph,
                f,
                indent=2,
                ensure_ascii=False
            )


        print(
            "AFFILIATE ASSET KNOWLEDGE GRAPH V5 CREATED"
        )

        print(
            "PRODUCTS:",
            len(
                canonical_products
            )
        )

        print(
            "LIVE ASSET ROWS:",
            len(
                live_assets
            )
        )

        print(
            "GENERATED ASSETS:",
            len(
                graph["assets"]
            )
        )

        print(
            "ROUTING ASSETS:",
            routing_assets_created
        )

        print(
            "WITHOUT ASSETS:",
            len(
                products_without_assets
            )
        )

        if products_without_assets:

            print(
                "MISSING:"
            )

            for product_id in products_without_assets:
                print(
                    "-",
                    product_id
                )


if __name__ == "__main__":

    AffiliateAssetKnowledgeBuilder().build()
