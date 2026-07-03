"""
FBEP Feed Sync

Prepares validated feed products for Google Sheets synchronization.
This module does not publish content.
"""

from typing import Any


FEED_SHEET_HEADERS = [
    "product_id",
    "source",
    "partner",
    "title",
    "description",
    "category",
    "price",
    "currency",
    "product_url",
    "affiliate_url",
    "image_url",
    "status",
    "brand",
    "tags",
    "commission_type",
    "commission_value",
    "tracking_id",
    "seo_title",
    "meta_description",
    "compliance_notes",
    "created_at",
    "updated_at",
]


def product_to_sheet_row(product: dict[str, Any]) -> list[Any]:
    return [product.get(header, "") for header in FEED_SHEET_HEADERS]


def products_to_sheet_rows(products: list[dict[str, Any]]) -> list[list[Any]]:
    return [product_to_sheet_row(product) for product in products]


def valid_results_to_sheet_rows(results: list[dict[str, Any]]) -> list[list[Any]]:
    valid_products = [
        result["product"]
        for result in results
        if result.get("valid") is True and "product" in result
    ]

    return products_to_sheet_rows(valid_products)


def invalid_results_to_error_rows(results: list[dict[str, Any]]) -> list[list[Any]]:
    rows: list[list[Any]] = []

    for result in results:
        if result.get("valid") is True:
            continue

        product = result.get("product", {})
        errors = result.get("errors", [])

        rows.append([
            product.get("product_id", ""),
            product.get("source", ""),
            product.get("title", ""),
            "validation_error",
            "; ".join(errors),
        ])

    return rows
