import json
from pathlib import Path


class KnowledgeAdapter:


    def __init__(self):

        self.master_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.source_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )

        self.knowledge_depth_file = Path(
            "data_master/content_intelligence/knowledge_depth_graph.json"
        )

        self.experience_file = Path(
            "data_master/content_intelligence/content_experience_intelligence_graph.json"
        )

        self.asset_file = Path(
            "data_master/content_intelligence/asset_selection_intelligence_graph.json"
        )

        self.validation_file = Path(
            "data_master/content_intelligence/production_validation_intelligence_graph.json"
        )


        self.master = self._load(self.master_file)
        self.questions = self._load(self.question_file)
        self.sources_graph = self._load(self.source_file)
        self.knowledge_depth = self._load(self.knowledge_depth_file)
        self.experience = self._load(self.experience_file)
        self.assets = self._load(self.asset_file)
        self.validation = self._load(self.validation_file)



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

        for product in self.master.get(
            "products",
            []
        ):

            if product.get("product_id") == product_id:
                return product

        return {}



    def _get_questions(self, product_id):

        result = []

        for item in self.questions.get(
            "questions",
            []
        ):

            if item.get("product_id") == product_id:
                result.append(item)

        return result



    def _build_summary(
        self,
        catalog,
        identity,
        llm_context
    ):

        summary = catalog.get(
            "summary",
            ""
        )

        if summary:
            return summary


        summary = llm_context.get(
            "summary",
            ""
        )

        if summary:
            return summary


        name = identity.get(
            "name",
            ""
        )

        category = identity.get(
            "category",
            ""
        )

        return (
            "Informationen zu "
            + name
            + " im Bereich "
            + category
            + " aus offiziellen Partnerinformationen."
        )



    def _build_key_facts(
        self,
        catalog,
        identity,
        llm_context
    ):

        facts = catalog.get(
            "key_facts",
            []
        )

        if facts:
            return facts


        llm_facts = llm_context.get(
            "facts",
            {}
        )


        result = []


        if llm_facts:

            result.append(
                "Produktinformationen aus offizieller Partnerquelle"
            )

            if llm_facts.get("category"):

                result.append(
                    "Kategorie: "
                    + llm_facts.get("category")
                )

            if llm_facts.get("source_reference"):

                result.append(
                    "Quelle: "
                    + llm_facts.get("source_reference")
                )


        return result



    def _get_faq(self, product_id):

        faq = []

        product = self._find_product(
            product_id
        )

        catalog = product.get(
            "catalog",
            {}
        )


        existing = catalog.get(
            "faq",
            []
        )

        if existing:
            return existing


        for q in self._get_questions(product_id):

            faq.append(
                {
                    "question": q.get(
                        "question",
                        ""
                    ),
                    "answer":
                        "Diese Information basiert auf der verfügbaren Wissensbasis und den hinterlegten Produktinformationen."
                }
            )


        return faq



    def _get_sources(self, product_id):

        product = self._find_product(
            product_id
        )

        catalog = product.get(
            "catalog",
            {}
        )


        existing = catalog.get(
            "sources",
            []
        )

        if existing:
            return existing


        result = []


        for item in self.sources_graph.get(
            "connections",
            {}
        ).get(
            "product_to_source",
            []
        ):

            if item.get(
                "product_id"
            ) == product_id:

                result.append(
                    item.get(
                        "source"
                    )
                )


        if not result:

            knowledge = product.get(
                "knowledge",
                {}
            )

            llm_context = knowledge.get(
                "llm_context",
                {}
            )

            source = llm_context.get(
                "source_reference"
            )

            if source:
                result.append(source)


        return result



    def _get_asset_selection(self, product_id):

        result = []

        for item in self.assets.get(
            "assets",
            []
        ):

            if item.get(
                "asset_id"
            ) == product_id:

                result.append(item)

        return result



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
        "tracking_url_v3",
        ""
    )
    or
    catalog.get(
        "tracking_url",
        ""
    )
    or
    catalog.get(
        "affiliate_url",
        ""
    ),

            "summary":
                self._build_summary(
                    catalog,
                    identity,
                    llm_context
                ),

            "hero_title":
                catalog.get(
                    "hero_title",
                    ""
                ),

            "content":
                catalog.get(
                    "content",
                    ""
                ),

            "comparison_matrix":
                catalog.get(
                    "comparison_matrix",
                    []
                ),

            "key_facts":
                self._build_key_facts(
                    catalog,
                    identity,
                    llm_context
                ),

            "faq":
                self._get_faq(
                    product_id
                ),

            "sources":
                self._get_sources(
                    product_id
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

            "questions":
                self._get_questions(
                    product_id
                ),

            "knowledge_depth":
                self.knowledge_depth,

            "content_experience":
                self.experience,

            "asset_selection":
                self._get_asset_selection(
                    product_id
                ),

            "production_validation":
                self.validation,

            "knowledge_status":
                master_product.get(
                    "status",
                    "READY"
                )
        }



if __name__ == "__main__":

    adapter = KnowledgeAdapter()

    result = adapter.build_product_context(
        "CHK24_004"
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
