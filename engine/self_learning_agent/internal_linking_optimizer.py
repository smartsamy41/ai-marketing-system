import json
from pathlib import Path


class InternalLinkingOptimizer:

    def __init__(
        self,
        rules_file="data_master/linking/internal_link_rules.json",
        category_file="data_master/linking/category_map.json",
        silo_file="data_master/linking/silo_structure.json"
    ):

        self.rules_file = Path(rules_file)
        self.category_file = Path(category_file)
        self.silo_file = Path(silo_file)

        self.rules = self._load_json(
            self.rules_file
        )

        self.categories = self._load_json(
            self.category_file
        )

        self.silos = self._load_json(
            self.silo_file
        )


    def _load_json(
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
            return json.load(file)



    def find_category(
        self,
        product_id
    ):

        for name, data in self.categories.get(
            "categories",
            {}
        ).items():

            if data.get("product_id") == product_id:
                return name

            if product_id in data.get(
                "product_ids",
                []
            ):
                return name

        return None



    def find_silo(
        self,
        category
    ):

        data = self.categories.get(
            "categories",
            {}
        ).get(
            category,
            {}
        )

        return data.get(
            "silo"
        )



    def suggest_links(
        self,
        article,
        products
    ):

        links = []

        article_category = article.get(
            "category"
        )


        article_silo = self.find_silo(
            article_category
        )


        max_links = self.rules.get(
            "internal_linking",
            {}
        ).get(
            "max_links_per_article",
            8
        )


        for product in products:


            product_id = product.get(
                "product_id"
            )


            category = self.find_category(
                product_id
            )


            silo = self.find_silo(
                category
            )


            priority = 20
            reason = "cross_silo"


            if category == article_category:

                priority = 100
                reason = "same_category"


            elif silo == article_silo:

                priority = 70
                reason = "same_silo"



            links.append(
                {
                    "from":
                        article.get(
                            "slug"
                        ),

                    "to":
                        product_id,

                    "category":
                        category,

                    "silo":
                        silo,

                    "priority":
                        priority,

                    "reason":
                        reason,

                    "status":
                        "suggested"
                }
            )


        links = sorted(
            links,
            key=lambda x: x["priority"],
            reverse=True
        )


        return {
            "links":
                links[:max_links],

            "count":
                len(
                    links[:max_links]
                )
        }



    def validate_link(
        self,
        link
    ):

        return {
            "link":
                link,

            "valid":
                True
        }



if __name__ == "__main__":


    optimizer = InternalLinkingOptimizer()


    result = optimizer.suggest_links(

        {
            "slug":
                "strom-ratgeber",

            "category":
                "strom"

        },


        [

            {
                "product_id":
                    "CHK24_001"
            },

            {
                "product_id":
                    "TC_001"
            },

            {
                "product_id":
                    "TC_009"
            }

        ]

    )


    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
