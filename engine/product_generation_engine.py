from datetime import datetime


class ProductGenerationEngine:

    def __init__(self):

        # =========================
        # BASE CATEGORIES
        # =========================
        self.categories = [
            "strom",
            "gas",
            "dsl",
            "kredit",
            "versicherung",
            "amazon"
        ]

    # =========================
    # SINGLE PRODUCT GENERATION
    # =========================
    def generate_product(self, category, index):

        product_id = f"{category.upper()}_{index:03d}"

        return {
            "product_id": product_id,
            "category": category,
            "title": f"{category} Vergleich 2026",
            "description": f"Beste {category} Angebote vergleichen",
            "status": "AUTO_GENERATED",
            "created_at": datetime.utcnow().isoformat()
        }

    # =========================
    # CATEGORY EXPANSION
    # =========================
    def expand_category(self, category, count=5):

        products = []

        for i in range(1, count + 1):

            products.append(
                self.generate_product(category, i)
            )

        return products

    # =========================
    # FULL PRODUCT GENERATION
    # =========================
    def build_all_products(self):

        all_products = []

        for cat in self.categories:

            expanded = self.expand_category(cat, count=3)

            all_products.extend(expanded)

        return {
            "status": "PRODUCTS_GENERATED",
            "count": len(all_products),
            "products": all_products,
            "timestamp": datetime.utcnow().isoformat()
        }
