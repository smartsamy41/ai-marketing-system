import json
import csv
from pathlib import Path


class AffiliateAssetKnowledgeBuilder:


    def __init__(self):

        self.assets_csv = Path(
            "system_scan/FINAL_COMPLETE_SCAN/sheets/affiliate_assets_FULL.csv"
        )

        self.rules_csv = Path(
            "system_scan/FINAL_COMPLETE_SCAN/sheets/affiliate_rules_FULL.csv"
        )

        self.product_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.output = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )



    def read_csv(self, path):

        rows=[]

        if path.exists():

            with open(
                path,
                encoding="utf-8-sig",
                newline=""
            ) as f:

                reader=csv.DictReader(f)

                for row in reader:
                    rows.append(row)

        return rows



    def read_json(self,path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def add_asset(
        self,
        graph,
        asset_id,
        product_name,
        asset_type,
        row
    ):

        asset={

            "asset_id":asset_id,

            "product_name":product_name,

            "source":asset_type,

            "status":row.get("status"),

            "direct_link":row.get("direktlink"),

            "calculator":row.get("vergleichsrechner_html"),

            "short_calculator":row.get("kurzrechner_html"),

            "banner_300x250":row.get("banner_300x250_html"),

            "banner_728x90":row.get("banner_728x90_html"),

            "tracking":row.get("tracking_hinweis"),

            "compliance":{

                "kennzeichnung":
                row.get("kennzeichnung"),

                "impressum":
                row.get("impressum_hinweis"),

                "verbote":
                row.get("verbote")
            }
        }


        graph["assets"].append(asset)



        graph["connections"]["asset_to_tracking"].append(

            {
                "asset_id":asset_id,
                "tracking":row.get("tracking_hinweis")
            }

        )



        graph["connections"]["asset_to_compliance"].append(

            {
                "asset_id":asset_id,

                "kennzeichnung":
                row.get("kennzeichnung"),

                "impressum":
                row.get("impressum_hinweis")
            }

        )



    def build(self):


        assets=self.read_csv(
            self.assets_csv
        )


        rules=self.read_csv(
            self.rules_csv
        )


        products=self.read_json(
            self.product_file
        )



        graph={

            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "affiliate_asset_knowledge_graph",


            "version":
            "4.0",


            "status":
            "ACTIVE",


            "rules":{

                "official_data_only":True,

                "no_fabricated_assets":True,

                "tracking_required":True,

                "compliance_required":True

            },


            "partners":[],


            "products":[],


            "assets":[],


            "partner_rules":[],


            "connections":{

                "product_to_asset":[],

                "asset_to_tracking":[],

                "asset_to_compliance":[],

                "partner_to_rule":[]

            }

        }



        partners=set()



        for p in products.get("entities",[]):

            graph["products"].append(

                {
                    "product_id":p.get("product_id"),

                    "name":p.get("name"),

                    "partner":p.get("partner")
                }

            )

            partners.add(
                p.get("partner")
            )



        graph["partners"]=sorted(
            list(partners)
        )



        for row in assets:


            product_id=row.get(
                "email_id"
            )


            name=row.get(
                "email"
            )



            created=[]



            if row.get("direktlink"):

                created.append(
                    ("DIRECT","Direktlink")
                )


            if row.get("vergleichsrechner_html"):

                created.append(
                    ("CALCULATOR","Vergleichsrechner/Formular")
                )


            if row.get("kurzrechner_html"):

                created.append(
                    ("SHORT","Kurzrechner")
                )


            if row.get("banner_300x250_html"):

                created.append(
                    ("BANNER_300","Banner 300x250")
                )


            if row.get("banner_728x90_html"):

                created.append(
                    ("BANNER_728","Banner 728x90")
                )



            if not created:

                created.append(
                    ("GENERAL",row.get("source"))
                )



            for suffix,asset_type in created:


                self.add_asset(

                    graph,

                    f"{product_id}_{suffix}",

                    name,

                    asset_type,

                    row

                )



        for rule in rules:


            graph["partner_rules"].append(rule)


            graph["connections"]["partner_to_rule"].append(

                {

                    "partner":
                    rule.get("partner"),

                    "rule_id":
                    rule.get("rule_id")

                }

            )



        for product in graph["products"]:


            matching=[]


            for asset in graph["assets"]:

                if asset["asset_id"].startswith(
                    product["product_id"]
                ):

                    matching.append(
                        asset["asset_id"]
                    )



            graph["connections"]["product_to_asset"].append(

                {

                    "product_id":
                    product["product_id"],


                    "assets":
                    matching

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
            "AFFILIATE ASSET KNOWLEDGE GRAPH V4 CREATED"
        )

        print(
            "PRODUCTS:",
            len(graph["products"])
        )

        print(
            "ASSETS:",
            len(graph["assets"])
        )

        print(
            "RULES:",
            len(graph["partner_rules"])
        )




if __name__=="__main__":

    AffiliateAssetKnowledgeBuilder().build()
