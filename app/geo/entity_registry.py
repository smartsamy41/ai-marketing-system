import json
from pathlib import Path


ENTITY_FILE = Path(
    "knowledge/entities/products.json"
)


class EntityRegistry:


    def __init__(self):

        self.products = []

        self.load()



    def load(self):

        if not ENTITY_FILE.exists():

            return


        with open(
            ENTITY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        self.products = data.get(
            "products",
            []
        )



    def get_all(self):

        return self.products



    def get_by_id(
        self,
        product_id: str
    ):

        for product in self.products:

            if product.get(
                "product_id"
            ) == product_id:

                return product


        return None



    def count(self):

        return len(
            self.products
        )



if __name__ == "__main__":

    registry = EntityRegistry()

    print(
        "ENTITY REGISTRY LOADED"
    )

    print(
        "Products:",
        registry.count()
    )
