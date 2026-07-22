from app.geo.integration_adapter import GEOIntegrationAdapter
from app.geo.geo_cache import GEOCache


class GEOService:


    def __init__(self):

        self.adapter = GEOIntegrationAdapter()

        self.cache = GEOCache()



    def get_product_jsonld(
        self,
        product_id: str
    ) -> str:


        cached = self.cache.get(
            product_id
        )


        if cached:

            return cached



        schema = self.adapter.get_product_schema(
            product_id
        )


        if schema:

            self.cache.set(
                product_id,
                schema
            )


        return schema



    def get_product_entity(
        self,
        product_id: str
    ):


        return self.adapter.get_product_entity(
            product_id
        )



if __name__ == "__main__":


    service = GEOService()


    result = service.get_product_jsonld(
        "CHK24_001"
    )


    print(
        "GEO SERVICE READY"
    )


    print(
        result
    )
