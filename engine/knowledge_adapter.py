import json
from pathlib import Path


class KnowledgeAdapter:


    def __init__(self):

        self.master_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.master = self._load(
            self.master_file
        )


    def _load(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def _find_product(self, product_id):

        for product in self.master.get("products", []):

            if product.get("product_id") == product_id:
                return product

        return {}



    def build_product_context(self, product_id):

        master_product = self._find_product(
            product_id
        )


        if not master_product:
            return {}



        identity = master_product.get(
            "identity",
            {}
        )


        catalog = master_product.get(
            "catalog",
            {}
        )


        knowledge = master_product.get(
            "knowledge",
            {}
        )


        validation = master_product.get(
            "validation",
            {}
        )


        llm_context = knowledge.get(
            "llm_context",
            {}
        )



        return {

            "product_id":
                master_product.get(
                    "product_id",
                    ""
                ),

            "name":
                identity.get(
                    "name",
                    ""
                ),

            "partner":
                identity.get(
                    "partner",
                    ""
                ),

            "category":
                identity.get(
                    "category",
                    ""
                ),

            "landingpage":
                catalog.get(
                    "landingpage",
                    ""
                ),

            "tracking_url":
                catalog.get(
                    "tracking_url",
                    ""
                ),

            "hero_title":
                catalog.get(
                    "hero_title",
                    identity.get(
                        "name",
                        ""
                    )
                ),

            "summary":
                catalog.get(
                    "summary",
                    ""
                ),

            "key_facts":
                catalog.get(
                    "key_facts",
                    []
                ),

            "comparison_matrix":
                catalog.get(
                    "comparison_matrix",
                    []
                ),

            "faq":
                catalog.get(
                    "faq",
                    []
                ),

            "sources":
                catalog.get(
                    "sources",
                    []
                ),

            "author":
                catalog.get(
                    "author",
                    "Redaktion Free Basics"
                ),

            "reviewed_by":
                catalog.get(
                    "reviewed_by",
                    ""
                ),

            "updated_at":
                catalog.get(
                    "updated_at",
                    ""
                ),

            "internal_links":
                catalog.get(
                    "internal_links",
                    []
                ),

            "entity":
                catalog.get(
                    "entity",
                    {}
                ),

            "facts":
                llm_context.get(
                    "facts",
                    {}
                ),

            "llm_context":
                llm_context,

            "product_facts_registry":
                knowledge.get(
                    "facts_registry",
                    {}
                ),

            "wikidata":
                knowledge.get(
                    "wikidata",
                    {}
                ),

            "mediawiki":
                knowledge.get(
                    "mediawiki",
                    {}
                ),

            "validation":
                validation,

            "knowledge_status":
                master_product.get(
                    "status",
                    "READY"
                )
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
