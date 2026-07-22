from app.geo.geo_service import GEOService


class GEOLandingpageHook:


    def __init__(self):

        self.geo = GEOService()



    def schema_for_product(
        self,
        product_id: str
    ) -> str:

        return self.geo.get_product_jsonld(
            product_id
        )



if __name__ == "__main__":


    hook = GEOLandingpageHook()


    schema = hook.schema_for_product(
        "CHK24_001"
    )


    print(
        "GEO LANDINGPAGE HOOK READY"
    )


    print(
        schema
    )
