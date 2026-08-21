import json

from pathlib import Path
from datetime import datetime, timezone

from engine.content_intelligence.geo_product_matcher import (
    GeoProductMatcher
)


class GeoCandidateMatrixBuilder:

    def __init__(self):

        self.geo_registry_file = Path(
            "data_master/geo_layer/geo_registry.json"
        )

        self.product_master_file = Path(
            "data_master/catalog/product_master_44.json"
        )

        self.category_map_file = Path(
            "data_master/linking/category_map.json"
        )

        self.output_file = Path(
            "data_master/geo_layer/geo_candidate_matrix.json"
        )

        self.matcher = GeoProductMatcher()


    # =========================================================
    # JSON
    # =========================================================

    @staticmethod
    def load_json(path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)


    @staticmethod
    def save_json(
        path,
        data
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(value):

        if value is None:
            return ""

        return str(value).strip()


    @staticmethod
    def normalize(value):

        return (
            str(value or "")
            .strip()
            .lower()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )


    # =========================================================
    # CATEGORY MAP
    # =========================================================

    def get_category_mapping(
        self,
        key
    ):

        data = self.load_json(
            self.category_map_file
        )

        return (
            data.get(
                "categories",
                {}
            )
            .get(
                key,
                {}
            )
            or {}
        )


    # =========================================================
    # LOCATION QUALITY
    # =========================================================

    @staticmethod
    def location_quality(
        location
    ):

        validation = (
            location.get(
                "validation",
                {}
            )
            or {}
        )

        return {

            "real_location":
                validation.get(
                    "real_location"
                )
                is True,

            "source_verified":
                validation.get(
                    "source_verified"
                )
                is True,

            "wikidata_verified":
                validation.get(
                    "wikidata_verified"
                )
                is True

        }


    # =========================================================
    # PARTNER POLICY
    # =========================================================

    def partner_policy(
        self,
        product
    ):

        partner = self.normalize(
            product.get(
                "partner"
            )
        )

        product_id = self.clean(
            product.get(
                "product_id"
            )
        )


        if partner == "amazon":

            return {
                "candidate_allowed": False,
                "geo_content_allowed": False,
                "conversion_target": "affiliate_product",
                "requires_local_data": False,
                "requires_local_relevance": False,
                "reason": "amazon_geo_pages_disabled"
            }


        if partner == "check24":

            return {
                "candidate_allowed": True,
                "geo_content_allowed": True,
                "conversion_target": "partner_comparison",
                "requires_local_data": True,
                "requires_local_relevance": True,
                "reason": "check24_verified_local_market_required"
            }


        if partner == "tarifcheck":

            return {
                "candidate_allowed": True,
                "geo_content_allowed": True,
                "conversion_target": "partner_comparison",
                "requires_local_data": True,
                "requires_local_relevance": True,
                "reason": "tarifcheck_verified_local_relevance_required"
            }


        if (
            partner == "telekom"
            or product_id.startswith(
                "TEL_"
            )
        ):

            return {
                "candidate_allowed": True,
                "geo_content_allowed": True,
                "conversion_target": "external_shop",
                "requires_local_data": True,
                "requires_local_relevance": True,
                "shop_url": (
                    product.get(
                        "shop_url"
                    )
                    or "https://free-basics.telekom-profis.de"
                ),
                "reason": "telekom_editorial_geo_external_shop"
            }


        return {
            "candidate_allowed": False,
            "geo_content_allowed": False,
            "conversion_target": "",
            "requires_local_data": True,
            "requires_local_relevance": True,
            "reason": "partner_geo_policy_missing"
        }


    # =========================================================
    # TELEKOM CANDIDATE
    # =========================================================

    def build_telekom_candidate(
        self,
        location,
        product,
        policy
    ):

        product_id = self.clean(
            product.get(
                "product_id"
            )
        )

        location_id = self.clean(
            location.get(
                "location_id"
            )
        )

        quality = self.location_quality(
            location
        )

        mapping = self.get_category_mapping(
            "telekom"
        )

        candidate_ready = all([
            quality.get(
                "real_location"
            ),
            quality.get(
                "source_verified"
            ),
            quality.get(
                "wikidata_verified"
            ),
            bool(
                mapping
            ),
            mapping.get(
                "type"
            ) == "external_shop",
            mapping.get(
                "landingpage"
            ) is False,
            policy.get(
                "candidate_allowed"
            ) is True
        ])


        return {

            "candidate_id":
                f"{product_id}:{location_id}",

            "status":
                (
                    "CANDIDATE"
                    if candidate_ready
                    else "BLOCKED"
                ),

            "product_id":
                product_id,

            "product_name":
                product.get(
                    "name",
                    ""
                ),

            "partner":
                "telekom",

            "category":
                "telekom",

            "silo":
                mapping.get(
                    "silo",
                    "telekom"
                ),

            "location_id":
                location_id,

            "location_name":
                location.get(
                    "name",
                    ""
                ),

            "postal_code":
                location.get(
                    "postal_code",
                    ""
                ),

            "state":
                location.get(
                    "state",
                    ""
                ),

            "country":
                location.get(
                    "country",
                    "Deutschland"
                ),

            "wikidata_id":
                (
                    location
                    .get(
                        "entity",
                        {}
                    )
                    .get(
                        "wikidata_id",
                        ""
                    )
                ),

            "geo_url":
                (
                    "https://freebasics.online/"
                    "telekom/"
                    + self.normalize(
                        product.get(
                            "name",
                            ""
                        )
                    )
                    + "/"
                    + self.normalize(
                        location.get(
                            "name",
                            ""
                        )
                    )
                    + "/"
                ),

            "policy":
                policy,

            "validation":
                {

                    "real_location":
                        quality.get(
                            "real_location",
                            False
                        ),

                    "source_verified":
                        quality.get(
                            "source_verified",
                            False
                        ),

                    "wikidata_verified":
                        quality.get(
                            "wikidata_verified",
                            False
                        ),

                    "product_match":
                        True,

                    "category_match":
                        bool(
                            mapping
                        ),

                    "search_intent_match":
                        True,

                    "partner_compliant":
                        True,

                    "candidate_allowed":
                        candidate_ready,

                    "local_data_available":
                        False,

                    "unique_content":
                        False,

                    "publish_allowed":
                        False
                }
        }


    # =========================================================
    # STANDARD CANDIDATE
    # =========================================================

    def build_standard_candidate(
        self,
        location,
        product,
        policy
    ):

        product_id = self.clean(
            product.get(
                "product_id"
            )
        )

        location_id = self.clean(
            location.get(
                "location_id"
            )
        )

        partner = self.normalize(
            product.get(
                "partner"
            )
        )

        match = self.matcher.match(
            location,
            product_id
        )

        matched = (
            match.get(
                "status"
            )
            == "MATCHED"
        )

        candidate_ready = all([

            matched,

            match.get(
                "real_location"
            )
            is True,

            match.get(
                "source_verified"
            )
            is True,

            match.get(
                "wikidata_verified"
            )
            is True,

            match.get(
                "product_match"
            )
            is True,

            match.get(
                "category_match"
            )
            is True,

            match.get(
                "search_intent_match"
            )
            is True,

            match.get(
                "partner_compliant"
            )
            is True

        ])


        return {

            "candidate_id":
                f"{product_id}:{location_id}",

            "status":
                (
                    "CANDIDATE"
                    if candidate_ready
                    else "BLOCKED"
                ),

            "product_id":
                product_id,

            "product_name":
                product.get(
                    "name",
                    ""
                ),

            "partner":
                partner,

            "category":
                match.get(
                    "category",
                    product.get(
                        "category",
                        ""
                    )
                ),

            "silo":
                match.get(
                    "silo",
                    ""
                ),

            "location_id":
                location_id,

            "location_name":
                location.get(
                    "name",
                    ""
                ),

            "postal_code":
                location.get(
                    "postal_code",
                    ""
                ),

            "state":
                location.get(
                    "state",
                    ""
                ),

            "country":
                location.get(
                    "country",
                    "Deutschland"
                ),

            "wikidata_id":
                (
                    location
                    .get(
                        "entity",
                        {}
                    )
                    .get(
                        "wikidata_id",
                        ""
                    )
                ),

            "geo_url":
                match.get(
                    "geo_url",
                    ""
                ),

            "policy":
                policy,

            "validation":
                {

                    "real_location":
                        match.get(
                            "real_location",
                            False
                        ),

                    "source_verified":
                        match.get(
                            "source_verified",
                            False
                        ),

                    "wikidata_verified":
                        match.get(
                            "wikidata_verified",
                            False
                        ),

                    "product_match":
                        match.get(
                            "product_match",
                            False
                        ),

                    "category_match":
                        match.get(
                            "category_match",
                            False
                        ),

                    "search_intent_match":
                        match.get(
                            "search_intent_match",
                            False
                        ),

                    "partner_compliant":
                        match.get(
                            "partner_compliant",
                            False
                        ),

                    "candidate_allowed":
                        candidate_ready,

                    "local_data_available":
                        False,

                    "unique_content":
                        False,

                    "publish_allowed":
                        False
                }
        }


    # =========================================================
    # BUILD ONE
    # =========================================================

    def build_candidate(
        self,
        location,
        product
    ):

        product_id = self.clean(
            product.get(
                "product_id"
            )
        )

        location_id = self.clean(
            location.get(
                "location_id"
            )
        )

        partner = self.normalize(
            product.get(
                "partner"
            )
        )

        policy = self.partner_policy(
            product
        )


        # AMAZON / UNKNOWN PARTNER
        if not policy.get(
            "candidate_allowed"
        ):

            quality = self.location_quality(
                location
            )

            return {

                "candidate_id":
                    f"{product_id}:{location_id}",

                "status":
                    "BLOCKED",

                "product_id":
                    product_id,

                "product_name":
                    product.get(
                        "name",
                        ""
                    ),

                "partner":
                    partner,

                "category":
                    product.get(
                        "category",
                        ""
                    ),

                "location_id":
                    location_id,

                "location_name":
                    location.get(
                        "name",
                        ""
                    ),

                "state":
                    location.get(
                        "state",
                        ""
                    ),

                "wikidata_id":
                    (
                        location
                        .get(
                            "entity",
                            {}
                        )
                        .get(
                            "wikidata_id",
                            ""
                        )
                    ),

                "policy":
                    policy,

                "validation":
                    {

                        "real_location":
                            quality.get(
                                "real_location",
                                False
                            ),

                        "source_verified":
                            quality.get(
                                "source_verified",
                                False
                            ),

                        "wikidata_verified":
                            quality.get(
                                "wikidata_verified",
                                False
                            ),

                        "candidate_allowed":
                            False,

                        "local_data_available":
                            False,

                        "unique_content":
                            False,

                        "publish_allowed":
                            False
                    }
            }


        # TELEKOM SONDERPFAD
        if (
            partner == "telekom"
            or product_id.startswith(
                "TEL_"
            )
        ):

            return self.build_telekom_candidate(
                location,
                product,
                policy
            )


        # CHECK24 / TARIFCHECK
        return self.build_standard_candidate(
            location,
            product,
            policy
        )


    # =========================================================
    # BUILD MATRIX
    # =========================================================

    def build(self):

        geo = self.load_json(
            self.geo_registry_file
        )

        product_data = self.load_json(
            self.product_master_file
        )

        locations = (
            geo.get(
                "locations",
                []
            )
            or []
        )

        products = (
            product_data.get(
                "products",
                []
            )
            or []
        )

        candidates = []

        for location in locations:

            for product in products:

                candidates.append(
                    self.build_candidate(
                        location,
                        product
                    )
                )


        allowed = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "CANDIDATE"
        ]

        blocked = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "BLOCKED"
        ]


        partner_stats = {}

        for candidate in candidates:

            partner = candidate.get(
                "partner",
                "unknown"
            )

            partner_stats.setdefault(
                partner,
                {
                    "total": 0,
                    "candidates": 0,
                    "blocked": 0
                }
            )

            partner_stats[
                partner
            ][
                "total"
            ] += 1

            if candidate.get(
                "status"
            ) == "CANDIDATE":

                partner_stats[
                    partner
                ][
                    "candidates"
                ] += 1

            else:

                partner_stats[
                    partner
                ][
                    "blocked"
                ] += 1


        output = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_candidate_matrix",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "candidate_is_not_publication":
                        True,

                    "verified_location_required":
                        True,

                    "product_match_required":
                        True,

                    "category_match_required":
                        True,

                    "search_intent_required":
                        True,

                    "partner_compliance_required":
                        True,

                    "local_data_required_for_publish":
                        True,

                    "unique_content_required_for_publish":
                        True,

                    "amazon_geo_pages":
                        False,

                    "telekom_geo_editorial_content":
                        True,

                    "telekom_conversion_target":
                        "external_shop",

                    "telekom_landingpage":
                        False
                },

            "summary":
                {

                    "locations":
                        len(
                            locations
                        ),

                    "products":
                        len(
                            products
                        ),

                    "matrix_size":
                        len(
                            candidates
                        ),

                    "candidates":
                        len(
                            allowed
                        ),

                    "blocked":
                        len(
                            blocked
                        ),

                    "published":
                        0
                },

            "partner_stats":
                partner_stats,

            "candidates":
                candidates,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }


        self.save_json(
            self.output_file,
            output
        )


        print(
            "GEO CANDIDATE MATRIX CREATED V2"
        )

        print(
            "LOCATIONS:",
            len(
                locations
            )
        )

        print(
            "PRODUCTS:",
            len(
                products
            )
        )

        print(
            "MATRIX:",
            len(
                candidates
            )
        )

        print(
            "CANDIDATES:",
            len(
                allowed
            )
        )

        print(
            "BLOCKED:",
            len(
                blocked
            )
        )

        print(
            "PUBLISHED: 0"
        )

        print(
            "PARTNERS:"
        )

        for partner, stats in sorted(
            partner_stats.items()
        ):

            print(
                partner,
                stats
            )


        return output


if __name__ == "__main__":

    GeoCandidateMatrixBuilder().build()
