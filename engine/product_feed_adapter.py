"""
FBEP Product Feed Adapter

Connects normalized Feed Engine products with the existing product layer format.
"""

from typing import Any


def feed_product_to_product_record(feed_product: dict[str, Any]) -> dict[str, Any]:
    return {
        "product_id": feed_product.get("product_id", ""),
        "product_name": feed_product.get("title", ""),
        "source": feed_product.get("source", ""),
        "partner": feed_product.get("partner", ""),
        "category": feed_product.get("category", ""),
        "affiliate_url": feed_product.get("affiliate_url", ""),
        "official_direct_link": feed_product.get("product_url", ""),
        "image_url": feed_product.get("image_url", ""),
        "status": feed_product.get("status", "draft"),
        "seo_title": feed_product.get("seo_title", ""),
        "meta_description": feed_product.get("meta_description", ""),
        "compliance_notes": feed_product.get("compliance_notes", ""),
        "created_at": feed_product.get("created_at", ""),
        "updated_at": feed_product.get("updated_at", ""),
    }


def feed_results_to_product_records(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []

    for result in results:
        if result.get("valid") is not True:
            continue

        product = result.get("product", {})
        records.append(feed_product_to_product_record(product))

    return records
