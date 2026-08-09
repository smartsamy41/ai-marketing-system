import json
from pathlib import Path


class PartnerProductionIntelligenceBuilder:


    def __init__(self):

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )

        self.product_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.content_file = Path(
            "data_master/content_intelligence/related_content_intelligence_graph.json"
        )

        self.navigation_file = Path(
            "data_master/content_intelligence/navigation_intelligence_graph.json"
        )

        self.output = Path(
            "data_master/content_intelligence/partner_production_intelligence_graph.json"
        )



    def load(self,path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):

        entity = self.load(
            self.entity_file
        )

        products = self.load(
            self.product_file
        )

        content = self.load(
            self.content_file
        )

        navigation = self.load(
            self.navigation_file
        )


        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "partner_production_intelligence_graph",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "rules":
            {

                "master_data_only":
                True,

                "no_old_content_copy":
                True,

                "official_partner_data_only":
                True,

                "telekom_shop_rule":
                True

            },


            "nodes":
            {

                "partners": [],

                "products": [],

                "content": [],

                "navigation": [],

                "assets": [],

                "tracking": []

            },


            "connections":
            {

                "partner_to_product": [],

                "product_to_content": [],

                "product_to_navigation": [],

                "product_to_asset": [],

                "product_to_tracking": []

            }

        }



        partner_set=set()


        for p in products.get(
            "entities",
            []
        ):

            pid=p.get(
                "product_id"
            )

            partner=p.get(
                "partner"
            )

            partner_set.add(
                partner
            )


            graph["nodes"]["products"].append(

                {

                    "product_id":
                    pid,

                    "name":
                    p.get("name"),

                    "partner":
                    partner,

                    "category":
                    p.get("category")

                }

            )


            graph["connections"]["partner_to_product"].append(

                {

                    "partner":
                    partner,

                    "product_id":
                    pid

                }

            )



        for partner in sorted(partner_set):

            graph["nodes"]["partners"].append(

                {

                    "name":
                    partner

                }

            )



        for item in content.get(
            "connections",
            {}
        ).get(
            "article_to_related_product",
            []
        ):

            graph["connections"]["product_to_content"].append(
                item
            )



        for item in navigation.get(
            "connections",
            {}
        ).get(
            "product_to_footer",
            []
        ):

            graph["connections"]["product_to_navigation"].append(
                item
            )



        for product in graph["nodes"]["products"]:

            graph["connections"]["product_to_asset"].append(

                {

                    "product_id":
                    product["product_id"],

                    "asset_status":
                    "MAPPING_FROM_AFFILIATE_ASSETS"

                }

            )


            graph["connections"]["product_to_tracking"].append(

                {

                    "product_id":
                    product["product_id"],

                    "tracking_status":
                    "MAPPING_FROM_TRACKING_SOURCE"

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
            "PARTNER PRODUCTION INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )



if __name__=="__main__":

    PartnerProductionIntelligenceBuilder().build()
