"""
FBEP Feed Validator

Validation layer for normalized feed products.
"""

from engine.feed_models import FeedProduct, FeedValidationResult, VALID_SOURCES


IMAGE_REQUIRED_SOURCES = {
    "spreadshop",
    "amazon",
}


def validate_feed_product(product: FeedProduct) -> FeedValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not product.product_id:
        errors.append("missing product_id")

    if not product.source:
        errors.append("missing source")
    elif product.source not in VALID_SOURCES:
        errors.append(f"invalid source: {product.source}")

    if not product.title:
        errors.append("missing title")

    if not product.product_url and not product.affiliate_url:
        errors.append("missing product_url or affiliate_url")

    if product.source in IMAGE_REQUIRED_SOURCES and not product.image_url:
        errors.append(f"missing image_url for source: {product.source}")

    if not product.status:
        errors.append("missing status")

    if product.source in {"check24", "tarifcheck"}:
        if not product.compliance_notes:
            warnings.append("missing compliance_notes for regulated affiliate source")

    if product.source == "telekom":
        if "telekom" not in product.partner.lower():
            warnings.append("telekom source should use Telekom partner label")

    return FeedValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )
