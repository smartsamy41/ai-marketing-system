import json
import os


class ProductLayer:

    def __init__(self):

        # zentrale Produktquelle (später Sheets/API)
        self.product_sources = {
            "check24": [
                "CHK24_001",
                "CHK24_002",
                "CHK24_003",
                "CHK24_004",
                "CHK24_005"
            ],
            "tarifcheck": [
                "TC_001",
                "TC_002",
                "TC_003",
                "TC_004",
                "TC_005"
            ],
            "amazon": [
                "AMZ_001",
                "AMZ_002",
                "AMZ_003"
            ]
        }

    # =========================
    # GET ALL PRODUCTS
    # =========================
    def get_all_products(self):

        all_products = []

        for partner, products in self.product_sources.items():
            for p in products:
                all_products.append({
                    "product_id": p,
                    "partner": partner
                })

        return all_products

    # =========================
    # FILTER BY PARTNER
    # =========================
    def get_by_partner(self, partner_name):

        return self.product_sources.get(partner_name, [])

    # =========================
    # SINGLE PRODUCT LOAD
    # =========================
    def load_product(self, product_id):

        return {
            "product_id": product_id,
            "status": "LOADED",
            "source": "product_layer"
        }
