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


        self.master = self._load(
            self.master_file
        )

        self.questions = self._load(
            self.question_file
        )

        self.knowledge_depth = self._load(
            self.knowledge_depth_file
        )

        self.experience = self._load(
            self.experience_file
        )

        self.assets = self._load(
            self.asset_file
        )

        self.validation = self._load(
            self.validation_file
        )



    def _load(
        self,
        path
    ):

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )



    def _find_product(
        self,
        product_id
    ):

        for product in self.master.get(
            "products",
            []
        ):

            if product.get(
                "product_id"
            ) == product_id:

                return product

        return {}



    def _get_questions(
        self,
        product_id
    ):

        result = []

        for item in self.questions.get(
            "questions",
            []
        ):

            if item.get(
                "product_id"
            ) == product_id:

                result.append(
                    item
                )

        return result



    def _get_asset_selection(
        self,
        product_id
    ):

        result = []

        for item in self.assets.get(
            "assets",
            []
        ):

            if item.get(
                "asset_id"
            ) == product_id:

                result.append(
                    item
                )

        return result



    def build_product_context(
        self,
        product_id
    ):


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



            # NEUE INTELLIGENCE LAYER


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
        "CHK24_001"
    )


    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
