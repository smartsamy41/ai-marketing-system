import json

from app.geo.entity_registry import EntityRegistry
from app.geo.fact_registry import FactRegistry


class GEOComposer:


    def __init__(self):

        self.entities = EntityRegistry()
        self.facts = FactRegistry()



    def build_product_entity(
        self,
        product_id: str
    ):

        entity = self.entities.get_by_id(
            product_id
        )

        fact = self.facts.get_by_product_id(
            product_id
        )


        if not entity:

            return None


        result = {

            "@context":
                "https://schema.org",

            "@type":
                "Product",

            "product_id":
                product_id,

            "name":
                entity.get(
                    "name",
                    ""
                ),

            "partner":
                entity.get(
                    "partner",
                    ""
                ),

            "category":
                entity.get(
                    "category",
                    ""
                ),

            "landingpage":
                entity.get(
                    "landingpage",
                    ""
                ),

            "tracking_available":
                fact.get(
                    "tracking_available",
                    False
                ) if fact else False,

            "asset_status":
                fact.get(
                    "asset_status",
                    ""
                ) if fact else "",

            "geo_ready":
                fact.get(
                    "geo_ready",
                    False
                ) if fact else False

        }


        return result



if __name__ == "__main__":


    composer = GEOComposer()


    product = composer.build_product_entity(
        "CHK24_001"
    )


    print(
        json.dumps(
            product,
            indent=2,
            ensure_ascii=False
        )
    )
