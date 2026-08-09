import json
from pathlib import Path


class EntityGraphPopulationBuilder:


    def __init__(self):

        self.product_file = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.asset_file = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )

        self.page_file = Path(
            "data_master/content_production/rendered_page_architecture.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.cluster_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.source_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )

        self.output_file = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )


    def load(self,path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def valid(self,value):

        if not value:
            return False

        if str(value).lower()=="nan":
            return False

        return True



    def build(self):

        products=self.load(self.product_file)
        assets=self.load(self.asset_file).get("assets",[])
        pages=self.load(self.page_file).get("pages",[])
        articles=self.load(self.article_file).get("articles",[])
        questions=self.load(self.question_file).get("questions",[])
        clusters=self.load(self.cluster_file).get("clusters",[])


        graph={

            "system":"FREE BASICS AI MARKETING SYSTEM",

            "type":"entity_graph",

            "version":"6.0",

            "status":"ACTIVE",

            "nodes":{

                "partners":[],
                "products":[],
                "categories":[],
                "topics":[],
                "questions":[],
                "articles":[],
                "landingpages":[],
                "affiliate_assets":[],
                "tracking_assets":[],
                "conversion_targets":[],
                "analytics_tracking":[]

            },


            "relationships":[]

        }



        partners=set()
        categories=set()



        for p in products.get("entities",[]):

            pid=p.get("product_id")

            partner=p.get("partner")

            category=p.get("category")


            graph["nodes"]["products"].append({

                "id":pid,
                "name":p.get("name"),
                "partner":partner,
                "category":category

            })


            if partner:

                partners.add(partner)

                graph["relationships"].append({

                    "from":partner,
                    "relation":"provides",
                    "to":pid

                })


            if category:

                categories.add(category)

                graph["relationships"].append({

                    "from":pid,
                    "relation":"belongs_to",
                    "to":category

                })



        for p in partners:

            graph["nodes"]["partners"].append({

                "id":p,
                "type":"Partner"

            })


        for c in categories:

            graph["nodes"]["categories"].append({

                "id":c,
                "type":"Category"

            })



        for t in clusters:

            graph["nodes"]["topics"].append(t)



        for q in questions:

            graph["nodes"]["questions"].append(q)

            graph["relationships"].append({

                "from":q.get("product_id"),
                "relation":"answers",
                "to":q.get("question_id")

            })



        for a in articles:

            graph["nodes"]["articles"].append(a)

            graph["relationships"].append({

                "from":a.get("product_id"),
                "relation":"has_content",
                "to":a.get("article_id")

            })



        for page in pages:

            pid=page.get("product_id")

            lp="LP_"+pid


            graph["nodes"]["landingpages"].append({

                "id":lp,
                "product_id":pid,
                "status":"READY"

            })


            graph["relationships"].append({

                "from":pid,
                "relation":"represented_by",
                "to":lp

            })



        for asset in assets:


            aid=asset.get("asset_id")

            pid=asset.get("product_id")


            graph["nodes"]["affiliate_assets"].append(asset)


            if pid:

                graph["relationships"].append({

                    "from":pid,
                    "relation":"has_asset",
                    "to":aid

                })



            tracking_id="TRACK_"+aid


            graph["nodes"]["tracking_assets"].append({

                "id":tracking_id,
                "asset_id":aid,
                "tracking":asset.get("tracking")

            })


            if pid:

                graph["relationships"].append({

                    "from":pid,
                    "relation":"measured_by",
                    "to":tracking_id

                })



            targets=[

                asset.get("direct_link"),
                asset.get("calculator"),
                asset.get("short_calculator")

            ]


            for target in targets:

                if self.valid(target):

                    cid="CONVERSION_"+aid


                    graph["nodes"]["conversion_targets"].append({

                        "id":cid,
                        "asset_id":aid,
                        "url":target

                    })


                    graph["relationships"].append({

                        "from":aid,
                        "relation":"converts_to",
                        "to":cid

                    })

                    break



        # GLOBAL TRACKING SYSTEM

        tracking_systems=[

            "Google Analytics",
            "Google Tag Manager",
            "Google Ads Conversion",
            "Bing UET",
            "Pinterest Conversion Tag",
            "TikTok Pixel",
            "YouTube Analytics"

        ]


        for t in tracking_systems:

            graph["nodes"]["analytics_tracking"].append({

                "id":t,
                "type":"AnalyticsSystem",
                "status":"REGISTERED"

            })



        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                graph,
                f,
                indent=2,
                ensure_ascii=False
            )



        print("ENTITY GRAPH V6 CREATED")


        for k,v in graph["nodes"].items():

            print(k,":",len(v))


        print(
            "RELATIONSHIPS:",
            len(graph["relationships"])
        )



if __name__=="__main__":

    EntityGraphPopulationBuilder().build()
