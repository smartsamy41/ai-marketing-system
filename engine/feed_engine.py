"""
FBEP Feed Engine

Normalizes raw feed records into FeedProduct objects and validates them.
"""

from typing import Any

from engine.feed_models import FeedProduct
from engine.feed_validator import validate_feed_product


class FeedEngine:
    """
    Core feed normalization engine.

    This engine does not publish content.
    It only returns normalized products with validation results.
    """

    def normalize_record(self, raw_record: dict[str, Any]) -> FeedProduct:
        return FeedProduct.from_dict(raw_record)

    def process_record(self, raw_record: dict[str, Any]) -> dict[str, Any]:
        product = self.normalize_record(raw_record)
        validation = validate_feed_product(product)

        return {
            "product": product.to_dict(),
            "valid": validation.valid,
            "errors": validation.errors,
            "warnings": validation.warnings,
        }

    def process_records(self, raw_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.process_record(record) for record in raw_records]
