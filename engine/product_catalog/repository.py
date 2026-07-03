"""
FBEP Product Catalog Repository
"""


class InMemoryProductRepository:

    def __init__(self):
        self.products = {}

    def save(self, product):
        self.products[product.fbep_product_id] = product
        return product

    def get(self, fbep_product_id):
        return self.products.get(fbep_product_id)

    def delete(self, fbep_product_id):
        return self.products.pop(fbep_product_id, None)

    def list_all(self):
        return list(self.products.values())

    def find_by_source(self, source, source_product_id):
        for product in self.products.values():
            if (
                product.source == source
                and product.source_product_id == source_product_id
            ):
                return product

        return None
