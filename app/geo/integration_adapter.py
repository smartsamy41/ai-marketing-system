from app.geo.geo_composer import GEOComposer
from app.geo.jsonld_bridge import build_product_jsonld


class GEOIntegrationAdapter:


    def __init__(self):

        self.composer = GEOComposer()



    def get_product_schema(
        self,
        product_id: str
    ) -> str:

        product = self.composer.build_product_entity(
            product_id
        )


        if not product:

            return ""


        return build_product_jsonld(
            product
        )



    def get_product_entity(
        self,
        product_id: str
    ):

        return self.composer.build_product_entity(
            product_id
        )



if __name__ == "__main__":


    adapter = GEOIntegrationAdapter()


    schema = adapter.get_product_schema(
        "CHK24_001"
    )


    print(
        "GEO ADAPTER READY"
    )


    print(
        schema
    )
