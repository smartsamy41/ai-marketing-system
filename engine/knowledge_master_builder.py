import json
from pathlib import Path
from datetime import datetime, timezone


class KnowledgeMasterBuilder:


    def __init__(self):

        self.base = Path("data_master")

        self.catalog_file = (
            self.base
            / "catalog"
            / "product_master_44.json"
        )

        self.llm_file = (
            self.base
            / "geo_and_entities"
            / "llm_knowledge_chunks.json"
        )

        self.facts_file = (
            self.base
            / "geo_and_entities"
            / "entity_registry"
            / "product_facts_registry.json"
        )

        self.wikidata_file = (
            self.base
            / "geo_and_entities"
            / "wikidata_entities.json"
        )

        self.mediawiki_file = (
            self.base
            / "geo_and_entities"
            / "mediawiki_knowledge_graph.json"
        )

        self.sources_file = (
            self.base
            / "geo_and_entities"
            / "primary_sources_index.json"
        )

        self.output_file = (
            self.base
            / "knowledge_master"
            / "product_knowledge_master.json"
        )



    def load(self, path):

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def find_by_id(
        self,
        items,
        product_id
    ):

        for item in items:

            if item.get("product_id") == product_id:

                return item

        return {}



    def build_product(
        self,
        product
    ):

        product_id = product.get(
            "product_id"
        )


        llm = self.find_by_id(
            self.llm.get("chunks", []),
            product_id
        )


        facts = self.find_by_id(
            self.facts.get("products", []),
            product_id
        )


        wikidata = self.find_by_id(
            self.wikidata.get("entities", []),
            product_id
        )


        mediawiki = self.find_by_id(
            self.mediawiki.get("nodes", []),
            product_id
        )


        validation = {

            "product_available":
                bool(product),

            "llm_context_available":
                bool(llm),

            "facts_available":
                bool(facts),

            "source_available":
                bool(
                    product.get("partner")
                ),

            "affiliate_available":
                bool(
                    product.get("tracking_url")
                ),

            "wikidata_status":
                wikidata.get(
                    "wikidata_status",
                    "not_found"
                ),

            "mediawiki_status":
                mediawiki.get(
                    "status",
                    "not_found"
                )

        }



        return {

            "product_id":
                product_id,


            "identity": {

                "name":
                    product.get("name", ""),

                "category":
                    product.get("category", ""),

                "partner":
                    product.get("partner", "")

            },


            "catalog":

                product,


            "knowledge": {

                "llm_context":
                    llm,

                "facts_registry":
                    facts,

                "wikidata":
                    wikidata,

                "mediawiki":
                    mediawiki

            },


            "validation":
                validation,


            "status":
                "READY",


            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }



    def build(self):

        self.catalog = self.load(
            self.catalog_file
        )

        self.llm = self.load(
            self.llm_file
        )

        self.facts = self.load(
            self.facts_file
        )

        self.wikidata = self.load(
            self.wikidata_file
        )

        self.mediawiki = self.load(
            self.mediawiki_file
        )

        self.sources = self.load(
            self.sources_file
        )


        products = self.catalog.get(
            "products",
            []
        )


        output = {

            "version":
                "1.0",

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "description":
                "Unified Product Knowledge Master",

            "rules": {

                "verified_data_only":
                    True,

                "source_required":
                    True,

                "no_fabricated_facts":
                    True

            },

            "products": [],

            "status":
                "READY"

        }


        for product in products:

            output["products"].append(

                self.build_product(
                    product
                )

            )


        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                output,
                f,
                indent=2,
                ensure_ascii=False
            )


        return output



if __name__ == "__main__":


    builder = KnowledgeMasterBuilder()


    result = builder.build()


    print(
        "Knowledge Master erstellt:"
    )

    print(
        len(
            result["products"]
        ),
        "Produkte"
    )

    print(
        "Datei:",
        builder.output_file
    )
