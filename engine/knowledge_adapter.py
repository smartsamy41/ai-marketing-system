import json
from pathlib import Path


class KnowledgeAdapter:

    def __init__(self):
        self.product_file = Path(
            "data_master/catalog/product_master_44.json"
        )

        self.llm_file = Path(
            "data_master/geo_and_entities/llm_knowledge_chunks.json"
        )

        self.source_file = Path(
            "data_master/geo_and_entities/primary_sources_index.json"
        )


    def load_json(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)


    def build_product_context(self, product_id):

        products = self.load_json(
            self.product_file
        )["products"]

        product = next(
            (
                p for p in products
                if p["product_id"] == product_id
            ),
            None
        )

        if not product:
            return None


        return {
            "product_id": product.get("product_id"),
            "name": product.get("name"),
            "partner": product.get("partner"),
            "category": product.get("category"),
            "landingpage": product.get("landingpage"),
            "tracking_url": product.get("tracking_url"),
            "knowledge_status": "READY"
        }


if __name__ == "__main__":

    adapter = KnowledgeAdapter()

    result = adapter.build_product_context(
        "CHK24_001"
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
