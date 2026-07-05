"""
FBEP Catalog Importer

Imports normalized feed products into the Unified Product Catalog.
"""

from typing import Any

from engine.product_catalog import CatalogProduct, ProductCatalog
from engine.product_catalog.models import ProductVariant


def feed_product_to_catalog_product(feed_product: dict[str, Any]) -> CatalogProduct:
    variants = []

    variant_count = int(feed_product.get("variant_count") or 0)

    if variant_count:
        variants.append(
            ProductVariant(
                variant_id=f"{feed_product.get('product_id', '')}_variants",
                title=f"{variant_count} variants",
                product_url=feed_product.get("product_url", ""),
                image_url=feed_product.get("image_url", ""),
                price=feed_product.get("price"),
                currency=feed_product.get("currency", "EUR"),
                status=feed_product.get("status", "active"),
            )
        )

    return CatalogProduct(
        fbep_product_id=f"FBEP-{feed_product.get('source', '').upper()}-{feed_product.get('product_id', '')}",
        title=feed_product.get("title", ""),
        source=feed_product.get("source", ""),
        source_product_id=feed_product.get("product_id", ""),
        partner=feed_product.get("partner", ""),
        category=feed_product.get("category", ""),
        status=feed_product.get("status", "draft"),
        description=feed_product.get("description", ""),
        product_url=feed_product.get("product_url", ""),
        affiliate_url=feed_product.get("affiliate_url", ""),
        image_url=feed_product.get("image_url", ""),
        tags=feed_product.get("tags", []),
        variants=variants,
        compliance_notes=feed_product.get("compliance_notes", ""),
    )


class CatalogImporter:
    """
    Imports feed products into ProductCatalog.
    """

    def __init__(self, catalog: ProductCatalog | None = None):
        self.catalog = catalog or ProductCatalog()

    def import_feed_product(self, feed_product: dict[str, Any]) -> CatalogProduct:
        catalog_product = feed_product_to_catalog_product(feed_product)

        existing = self.catalog.get_product(catalog_product.fbep_product_id)

        if existing:
            return self.catalog.update_product(
                catalog_product.fbep_product_id,
                title=catalog_product.title,
                category=catalog_product.category,
                status=catalog_product.status,
                description=catalog_product.description,
                product_url=catalog_product.product_url,
                affiliate_url=catalog_product.affiliate_url,
                image_url=catalog_product.image_url,
                tags=catalog_product.tags,
                variants=catalog_product.variants,
                compliance_notes=catalog_product.compliance_notes,
            )

        return self.catalog.register_product(catalog_product)

    def import_feed_products(self, feed_products: list[dict[str, Any]]) -> list[CatalogProduct]:
        imported = []

        for feed_product in feed_products:
            imported.append(self.import_feed_product(feed_product))

        return imported
