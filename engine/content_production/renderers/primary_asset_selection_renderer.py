import json
from pathlib import Path
from datetime import datetime, timezone


class PrimaryAssetSelectionRenderer:


    def __init__(self):

        self.source = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )

        self.output = Path(
            "data_master/content_production/primary_asset_selection"
        )


    def load_data(self):

        with open(
            self.source,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def find_product_assets(
        self,
        product_id,
        assets
    ):

        result=[]

        for asset in assets:

            if asset.get("asset_id","").startswith(
                product_id
            ):

                result.append(asset)


        return result



    def select_primary_asset(
        self,
        product,
        assets
    ):


        partner = product["partner"]



        priority=[

            "Vergleichsrechner/Formular",

            "Kurzrechner",

            "Direktlink",

            "Banner 300x250",

            "Banner 728x90"

        ]



        if partner in [
            "check24",
            "tarifcheck"
        ]:


            for p in priority:

                for asset in assets:

                    if asset.get("source")==p:

                        return asset



        if partner=="amazon":

            return {

                "asset_id":
                product["product_id"],

                "source":
                "amazon_product"

            }



        if partner=="telekom":

            return {

                "asset_id":
                "TEL_SHOP_001",

                "source":
                "shop"

            }



        return None



    def build(self):


        data=self.load_data()


        products=data["products"]

        assets=data["assets"]


        result={}



        for product in products:


            product_id=product["product_id"]


            product_assets=self.find_product_assets(

                product_id,

                assets

            )


            primary=self.select_primary_asset(

                product,

                product_assets

            )



            if primary:


                result[product_id]={


                    "product_id":
                    product_id,


                    "product_name":
                    product["name"],


                    "partner":
                    product["partner"],


                    "primary_asset":{


                        "asset_id":
                        primary.get("asset_id"),


                        "source":
                        primary.get("source")

                    },


                    "available_assets":
                    len(product_assets)

                }



        output={


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "version":
            "PRIMARY_ASSET_SELECTION_V5",


            "created":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "products":
            result,


            "statistics":{


                "products_available":
                len(products),


                "assets_available":
                len(assets),


                "primary_assets_selected":
                len(result)

            }

        }



        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(

            self.output /
            "primary_asset_selection_graph.json",

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                output,

                f,

                indent=2,

                ensure_ascii=False

            )



        print(
            "PRIMARY ASSET SELECTION V5 CREATED"
        )

        print(
            "PRODUCTS:",
            len(products)
        )

        print(
            "ASSETS:",
            len(assets)
        )

        print(
            "SELECTED:",
            len(result)
        )



if __name__=="__main__":

    PrimaryAssetSelectionRenderer().build()
