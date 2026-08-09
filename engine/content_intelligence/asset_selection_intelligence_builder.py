import json
from pathlib import Path


class AssetSelectionIntelligenceBuilder:


    def __init__(self):

        self.asset_graph = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )


        self.output = Path(
            "data_master/content_intelligence/asset_selection_intelligence_graph.json"
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


        asset_data = self.load_json(
            self.asset_graph
        )


        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "asset_selection_intelligence",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "selection_rules":
            {


                "mobile":

                {

                    "preferred_assets":
                    [

                        "banner_300x250",

                        "kurzrechner",

                        "vergleichsrechner"

                    ],

                    "avoid":

                    [

                        "banner_728x90"

                    ]

                },


                "desktop":

                {

                    "preferred_assets":
                    [

                        "banner_728x90",

                        "banner_300x250",

                        "vergleichsrechner"

                    ]

                },


                "tablet":

                {

                    "preferred_assets":
                    [

                        "banner_300x250",

                        "vergleichsrechner"

                    ]

                }


            },


            "page_rules":
            {


                "article":

                [

                    "vergleichsrechner",

                    "banner_300x250",

                    "related_asset"

                ],


                "landingpage":

                [

                    "primary_conversion_asset",

                    "banner",

                    "calculator"

                ],


                "footer":

                [

                    "disclosure",

                    "partner_information"

                ]

            },


            "assets": [],


            "connections":
            {

                "product_to_asset_choice":

                [],


                "asset_to_device":

                [],


                "asset_to_position":

                []

            }

        }



        for asset in asset_data.get(
            "assets",
            []
        ):


            asset_id = asset.get(
                "asset_id"
            )


            item = {


                "asset_id":

                asset_id,


                "product":

                asset.get("product_name"),


                "available":

                []


            }



            if asset.get("banner_300x250"):

                item["available"].append(
                    "banner_300x250"
                )


            if asset.get("banner_728x90"):

                item["available"].append(
                    "banner_728x90"
                )


            if asset.get("calculator"):

                item["available"].append(
                    "vergleichsrechner"
                )


            if asset.get("short_calculator"):

                item["available"].append(
                    "kurzrechner"
                )


            if asset.get("direct_link"):

                item["available"].append(
                    "direktlink"
                )


            graph["assets"].append(
                item
            )



            for device in [
                "mobile",
                "desktop",
                "tablet"
            ]:


                graph["connections"]["asset_to_device"].append(

                    {

                        "asset_id":
                        asset_id,


                        "device":
                        device

                    }

                )



            graph["connections"]["asset_to_position"].append(

                {

                    "asset_id":
                    asset_id,


                    "positions":

                    [

                        "content",

                        "sidebar",

                        "footer"

                    ]

                }

            )



        for product in asset_data.get(
            "products",
            []
        ):


            graph["connections"]["product_to_asset_choice"].append(

                {

                    "product_id":
                    product.get("product_id"),


                    "selection":
                    "AUTO"

                }

            )



        self.output.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        with open(

            self.output,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                graph,

                f,

                indent=2,

                ensure_ascii=False

            )



        print(
            "ASSET SELECTION INTELLIGENCE GRAPH CREATED"
        )


        print(
            "ASSETS:",
            len(graph["assets"])
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__ == "__main__":

    AssetSelectionIntelligenceBuilder().build()
