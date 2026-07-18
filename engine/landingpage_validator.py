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


class LandingpageValidator:

    """
    MLP005 Core Landingpage Validator V1

    Read-only validation layer.
    No database writes.
    No sheet changes.
    """

    def validate(
        self,
        landingpage: dict[str, Any],
        partner: str | None = None
    ) -> dict[str, Any]:

        errors = []
        warnings = []

        product_id = str(
            landingpage.get("product_id") or ""
        )

        source = str(
            partner or landingpage.get("partner") or ""
        ).lower()


        # Telekom Sonderregel:
        # keine eigene Produktlandingpage notwendig

        if source == "telekom" or product_id.startswith("TEL_"):

            return {
                "status": "COMPLIANT",
                "product_id": product_id,
                "errors": [],
                "warnings": [
                    "Telekom redirect rule applied"
                ]
            }


        for field in CORE_REQUIRED_FIELDS:

            value = str(
                landingpage.get(field) or ""
            ).strip()

            if not value:
                errors.append(
                    f"missing:{field}"
                )


        missing_seo = []

        for field in SEO_FIELDS:

            if not str(
                landingpage.get(field) or ""
            ).strip():

                missing_seo.append(field)


        missing_content = []

        for field in CONTENT_FIELDS:

            if not str(
                landingpage.get(field) or ""
            ).strip():

                missing_content.append(field)


        if missing_seo:
            warnings.append(
                "seo_missing:"
                + ",".join(missing_seo)
            )


        if missing_content:
            warnings.append(
                "content_missing:"
                + ",".join(missing_content)
            )


        return {
            "status": (
                "BLOCKED"
                if errors
                else "COMPLIANT"
            ),
            "product_id": product_id,
            "errors": errors,
            "warnings": warnings
        }
