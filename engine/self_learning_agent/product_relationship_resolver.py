import json
from pathlib import Path


class ProductRelationshipResolver:


    def __init__(
        self,
        catalog_file="data_master/catalog/product_master_44.json",
        category_file="data_master/linking/category_map.json",
        silo_file="data_master/linking/silo_structure.json"
    ):

        self.catalog_file = Path(catalog_file)
        self.category_file = Path(category_file)
        self.silo_file = Path(silo_file)

        self.catalog = self.load_json(
            self.catalog_file
        )

        self.category_map = self.load_json(
            self.category_file
        ).get(
            "categories",
            {}
        )

        self.silos = self.load_json(
            self.silo_file
        ).get(
            "silos",
            {}
        )


    def load_json(
        self,
        path
    ):

        if not path.exists():

            return {}

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )



    def find_category(
        self,
        product
    ):

        product_id = product.get(
            "product_id"
        )


        for category, data in self.category_map.items():


            if data.get(
                "product_id"
            ) == product_id:

                return category



            if product_id in data.get(
                "product_ids",
                []
            ):

                return category



        return product.get(
            "category",
            ""
        ).lower()



    def resolve(
        self,
        product
    ):


        product_id = product.get(
            "product_id",
            ""
        )


        category = self.find_category(
            product
        )



        category_data = self.category_map.get(
            category,
            {}
        )


        silo = category_data.get(
            "silo",
            ""
        )


        related_ids = self.silos.get(
            silo,
            {}
        ).get(
            "products",
            []
        )


        related_products = []


        for item_id in related_ids:


            if item_id == product_id:

                continue


            for item in self.catalog.get(
                "products",
                []
            ):


                if item.get(
                    "product_id"
                ) == item_id:


                    related_products.append(

                        {

                            "product_id":
                                item.get(
                                    "product_id"
                                ),

                            "category":
                                item.get(
                                    "category"
                                ),

                            "partner":
                                item.get(
                                    "partner"
                                )

                        }

                    )


        return {


            "product_id":
                product_id,


            "category":
                category,


            "silo":
                silo,


            "related_products":
                related_products[:8],


            "newsletter_segment":
                silo or category,


            "type":
                product.get(
                    "partner",
                    "affiliate"
                )

        }



if __name__ == "__main__":


    resolver = ProductRelationshipResolver()


    print(

        json.dumps(

            resolver.resolve(

                {

                    "product_id":
                        "CHK24_001",

                    "category":
                        "Strom",

                    "partner":
                        "check24"

                }

            ),

            indent=2,

            ensure_ascii=False

        )

    )
