"""
FBEP Product Catalog Core
"""

from dataclasses import replace

from engine.product_catalog.models import CatalogProduct, utc_now
from engine.product_catalog.repository import InMemoryProductRepository


class ProductCatalog:

    def __init__(self, repository=None):
        self.repository = repository or InMemoryProductRepository()

    def register_product(self, product: CatalogProduct):
        existing = self.repository.get(product.fbep_product_id)

        if existing:
            return existing

        return self.repository.save(product)

    def update_product(self, fbep_product_id, **updates):
        product = self.repository.get(fbep_product_id)

        if not product:
            return None

        updates["updated_at"] = utc_now()
        updated = replace(product, **updates)

        return self.repository.save(updated)

    def get_product(self, fbep_product_id):
        return self.repository.get(fbep_product_id)

    def find_by_source(self, source, source_product_id):
        return self.repository.find_by_source(source, source_product_id)

    def list_products(self):
        return self.repository.list_all()

    def delete_product(self, fbep_product_id):
        return self.repository.delete(fbep_product_id)
