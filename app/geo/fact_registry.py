import json
from pathlib import Path


FACT_FILE = Path(
    "knowledge/facts/product_facts.json"
)


class FactRegistry:


    def __init__(self):

        self.facts = []

        self.load()



    def load(self):

        if not FACT_FILE.exists():

            return


        with open(
            FACT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        self.facts = data.get(
            "facts",
            []
        )



    def get_all(self):

        return self.facts



    def get_by_product_id(
        self,
        product_id: str
    ):

        for fact in self.facts:

            if fact.get(
                "product_id"
            ) == product_id:

                return fact


        return None



    def count(self):

        return len(
            self.facts
        )



if __name__ == "__main__":

    registry = FactRegistry()

    print(
        "FACT REGISTRY LOADED"
    )

    print(
        "Facts:",
        registry.count()
    )
