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

        self.wikidata_file = Path(
            "data_master/geo_and_entities/wikidata_entities.json"
        )


    def load_json(self, file):

        if not file.exists():
            return {}

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)


    def find_llm_context(self, product_id):

        data = self.load_json(
            self.llm_file
        )

        chunks = data.get(
            "chunks",
            []
        )

        for chunk in chunks:

            if chunk.get("product_id") == product_id:

                return chunk

        return {}


    def find_source_context(self, product_id):

        data = self.load_json(
            self.source_file
        )

        if isinstance(data, dict):

            for item in data.get("sources", []):

                if item.get("product_id") == product_id:
                    return item

        return {}


    def find_wikidata_context(self, product_id):

        data = self.load_json(
            self.wikidata_file
        )

        if isinstance(data, dict):

            entities = data.get(
                "entities",
                []
            )

            for entity in entities:

                if entity.get("product_id") == product_id:
                    return entity

        return {}


    def build_product_context(
        self,
        product_id
    ):

        products = self.load_json(
            self.product_file
        ).get(
            "products",
            []
        )


        product = next(
            (
                p for p in products
                if p.get("product_id") == product_id
            ),
            None
        )


        if not product:
            return None



        llm_context = self.find_llm_context(
            product_id
        )


        source_context = self.find_source_context(
            product_id
        )


        wikidata_context = self.find_wikidata_context(
            product_id
        )


        facts = llm_context.get(
            "facts",
            {}
        )


        return {

            "product_id":
                product.get("product_id"),


            "name":
                product.get("name"),


            "partner":
                product.get("partner"),


            "category":
                product.get("category"),


            "landingpage":
                product.get("landingpage"),


            "tracking_url":
                product.get("tracking_url"),


            "facts":
                facts,


            "llm_context":
                llm_context,


            "sources":
                source_context,


            "wikidata":
                wikidata_context,


            "knowledge_status":
                "READY"

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
