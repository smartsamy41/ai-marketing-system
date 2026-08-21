from typing import Any


CORE_REQUIRED_FIELDS = [
    "product_id",
    "product_name",
    "seo_title",
    "meta_description",
    "html",
    "affiliate_url",
    "status",
    "version",
]


SEO_FIELDS = [
    "canonical_url",
    "structured_data",
    "open_graph",
    "twitter_card",
]


CONTENT_FIELDS = [
    "hero_title",
    "hero_description",
    "problem_section",
    "solution_section",
]


GEO_REQUIRED_FLAGS = [
    "real_location",
    "source_verified",
    "wikidata_verified",
    "product_match",
    "category_match",
    "search_intent_match",
    "local_data_available",
    "partner_compliant",
    "unique_content",
]


class LandingpageValidator:

    """
    FREE BASICS AI MARKETING SYSTEM

    Central Landingpage + GEO Quality Shield.

    Rules:
    - Normal product pages use existing validation.
    - GEO pages require verified local data.
    - No fabricated local content.
    - Failed GEO nodes remain NOINDEX,FOLLOW.
    - Only validated GEO nodes may enter sitemap / llms feeds.
    """


    @staticmethod
    def _truthy(value):

        if isinstance(value, bool):
            return value

        text = str(
            value or ""
        ).strip().lower()

        return text in {
            "true",
            "1",
            "yes",
            "ja",
            "verified",
            "valid",
            "pass",
            "ready"
        }


    def validate_geo(
        self,
        landingpage: dict[str, Any]
    ) -> dict[str, Any]:

        product_id = str(
            landingpage.get("product_id")
            or ""
        ).strip()


        failed = []


        for field in GEO_REQUIRED_FLAGS:

            if not self._truthy(
                landingpage.get(field)
            ):

                failed.append(field)


        location_id = str(
            landingpage.get("location_id")
            or ""
        ).strip()


        location_name = str(
            landingpage.get("location_name")
            or landingpage.get("city")
            or ""
        ).strip()


        if not location_id:
            failed.append(
                "location_id"
            )


        if not location_name:
            failed.append(
                "location_name"
            )


        if failed:

            return {

                "status":
                    "COMPLIANT",

                "product_id":
                    product_id,

                "page_type":
                    "geo",

                "geo_quality_status":
                    "NOINDEX",

                "robots":
                    "noindex, follow",

                "sitemap_allowed":
                    False,

                "llms_allowed":
                    False,

                "indexnow_allowed":
                    False,

                "geo_publish_allowed":
                    False,

                "errors":
                    [],

                "warnings":
                    [
                        "geo_quality_shield_failed:"
                        + ",".join(
                            sorted(
                                set(failed)
                            )
                        )
                    ]

            }


        return {

            "status":
                "COMPLIANT",

            "product_id":
                product_id,

            "page_type":
                "geo",

            "geo_quality_status":
                "INDEX",

            "robots":
                "index, follow",

            "sitemap_allowed":
                True,

            "llms_allowed":
                True,

            "indexnow_allowed":
                True,

            "geo_publish_allowed":
                True,

            "errors":
                [],

            "warnings":
                []

        }


    def validate(
        self,
        landingpage: dict[str, Any],
        partner: str | None = None
    ) -> dict[str, Any]:

        errors = []

        warnings = []


        product_id = str(
            landingpage.get("product_id")
            or ""
        ).strip()


        source = str(
            partner
            or landingpage.get("partner")
            or ""
        ).strip().lower()


        page_type = str(
            landingpage.get("page_type")
            or ""
        ).strip().lower()


        # =====================================================
        # GEO QUALITY SHIELD
        # =====================================================

        if page_type == "geo":

            return self.validate_geo(
                landingpage
            )


        # =====================================================
        # TELEKOM SPECIAL RULE
        # =====================================================

        if (
            source == "telekom"
            or product_id.startswith(
                "TEL_"
            )
        ):

            return {

                "status":
                    "COMPLIANT",

                "product_id":
                    product_id,

                "page_type":
                    "editorial",

                "robots":
                    "index, follow",

                "sitemap_allowed":
                    True,

                "llms_allowed":
                    True,

                "errors":
                    [],

                "warnings":
                    [
                        "Telekom direct-shop routing rule applied"
                    ]

            }


        # =====================================================
        # EXISTING PRODUCT LANDINGPAGE VALIDATION
        # =====================================================

        for field in CORE_REQUIRED_FIELDS:

            value = str(
                landingpage.get(field)
                or ""
            ).strip()

            if not value:

                errors.append(
                    f"missing:{field}"
                )


        missing_seo = []


        for field in SEO_FIELDS:

            if not str(
                landingpage.get(field)
                or ""
            ).strip():

                missing_seo.append(
                    field
                )


        missing_content = []


        for field in CONTENT_FIELDS:

            if not str(
                landingpage.get(field)
                or ""
            ).strip():

                missing_content.append(
                    field
                )


        if missing_seo:

            warnings.append(

                "seo_missing:"
                + ",".join(
                    missing_seo
                )

            )


        if missing_content:

            warnings.append(

                "content_missing:"
                + ",".join(
                    missing_content
                )

            )


        blocked = bool(
            errors
        )


        return {

            "status":
                (
                    "BLOCKED"
                    if blocked
                    else "COMPLIANT"
                ),

            "product_id":
                product_id,

            "page_type":
                "product",

            "robots":
                (
                    "noindex, follow"
                    if blocked
                    else "index, follow"
                ),

            "sitemap_allowed":
                not blocked,

            "llms_allowed":
                not blocked,

            "errors":
                errors,

            "warnings":
                warnings

        }


if __name__ == "__main__":

    validator = LandingpageValidator()


    print(
        validator.validate(
            {
                "product_id":
                    "CHK24_001",

                "page_type":
                    "geo",

                "location_id":
                    "DE-SH-LUEBECK",

                "location_name":
                    "Lübeck",

                "real_location":
                    True,

                "source_verified":
                    True,

                "wikidata_verified":
                    True,

                "product_match":
                    True,

                "category_match":
                    True,

                "search_intent_match":
                    True,

                "local_data_available":
                    True,

                "partner_compliant":
                    True,

                "unique_content":
                    True
            },
            partner="check24"
        )
    )
