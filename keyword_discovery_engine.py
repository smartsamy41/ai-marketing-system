from datetime import datetime


class KeywordDiscoveryEngine:

    def __init__(self):

        # =========================
        # BASE SEEDS (START POINTS)
        # =========================
        self.seed_keywords = [
            "strom tarif",
            "gas vergleich",
            "dsl internet",
            "kredit zinsen",
            "versicherung auto",
            "amazon deals",
            "beste anbieter",
            "tarif wechseln",
            "kosten sparen"
        ]

        self.generated_keywords = []

    # =========================
    # EXPAND KEYWORD
    # =========================
    def expand_keyword(self, keyword):

        variations = [
            f"{keyword} 2026",
            f"beste {keyword}",
            f"{keyword} vergleich",
            f"{keyword} anbieter",
            f"günstige {keyword}",
            f"{keyword} wechseln"
        ]

        return variations

    # =========================
    # DISCOVER KEYWORDS
    # =========================
    def discover(self):

        all_keywords = []

        for seed in self.seed_keywords:

            expanded = self.expand_keyword(seed)

            for k in expanded:

                all_keywords.append({
                    "keyword": k,
                    "source": seed,
                    "status": "DISCOVERED"
                })

        self.generated_keywords = all_keywords

        return {
            "status": "KEYWORDS_DISCOVERED",
            "count": len(all_keywords),
            "keywords": all_keywords,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================
    # CONVERT TO PRODUCTS
    # =========================
    def to_products(self):

        products = []

        for i, item in enumerate(self.generated_keywords):

            keyword = item["keyword"]

            product_id = f"KW_{i:04d}"

            products.append({
                "product_id": product_id,
                "title": f"{keyword} Vergleich 2026",
                "category": "keyword_based",
                "keyword": keyword,
                "status": "AUTO_GENERATED_FROM_KEYWORD"
            })

        return {
            "status": "KEYWORDS_TO_PRODUCTS_DONE",
            "count": len(products),
            "products": products
        }
