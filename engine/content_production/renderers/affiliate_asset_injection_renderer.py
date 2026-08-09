import json
from pathlib import Path
from datetime import datetime, timezone


class AffiliateAssetInjectionRenderer:


    def __init__(self):

        self.source = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )

        self.output = Path(
            "data_master/content_production/affiliate_asset_output"
        )



    def load_json(self,path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):


        data = self.load_json(
            self.source
        )


        assets = data.get(
            "assets",
            []
        )


        connections = data.get(
            "connections",
            {}
        )


        product_asset_links = connections.get(
            "product_to_asset",
            []
        )


        tracking_links = connections.get(
            "asset_to_tracking",
            []
        )


        compliance_links = connections.get(
            "asset_to_compliance",
            []
        )


        products = {}


        asset_lookup = {}


        for asset in assets:


            asset_id = asset.get(
                "asset_id"
            )


            if asset_id:

                asset_lookup[asset_id]=asset



        for link in product_asset_links:


            product_id = link.get(
                "product_id"
            )


            asset_id = link.get(
                "asset_id"
            )


            if not product_id:

                continue



            if product_id not in products:

                products[product_id]=[]



            asset = asset_lookup.get(
                asset_id,
                {}
            )


            products[product_id].append(

                {

                    "asset_id":
                    asset_id,


                    "partner":
                    asset.get(
                        "partner"
                    ),


                    "asset_type":
                    asset.get(
                        "asset_type"
                    ),


                    "tracking_required":
                    True,


                    "advertising_label_required":
                    True

                }

            )



        result = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "affiliate_asset_injection",


            "version":
            "2.0",


            "created":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "status":
            "ACTIVE",


            "rules":
            {

                "official_assets_only":
                True,


                "no_fabricated_assets":
                True,


                "tracking_required":
                True,


                "advertising_disclosure_required":
                True

            },


            "products":
            products,


            "connections":
            {

                "product_to_asset":
                product_asset_links,


                "asset_to_tracking":
                tracking_links,


                "asset_to_compliance":
                compliance_links

            }

        }



        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        file = self.output / "affiliate_asset_injection_graph.json"


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                result,
                f,
                indent=2,
                ensure_ascii=False
            )



        print(
            "AFFILIATE ASSET INJECTION GRAPH CREATED V2"
        )

        print(
            "PRODUCTS:",
            len(products)
        )

        print(
            "ASSETS:",
            len(assets)
        )


        for k,v in result["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__=="__main__":

    AffiliateAssetInjectionRenderer().build()
