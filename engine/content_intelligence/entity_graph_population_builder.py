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

        self.primary_asset_file = Path(
            "data_master/content_production/primary_asset_selection/primary_asset_selection_graph.json"
        )

        self.landingpage_folder = Path(
            "data_master/content_production/final_pages"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.cluster_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.source_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )

        self.output_file = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):

        products = self.load_json(
            self.product_file
        )

        assets_graph = self.load_json(
            self.asset_file
        )

        primary_assets = self.load_json(
            self.primary_asset_file
        )

        articles = self.load_json(
            self.article_file
        )

        clusters = self.load_json(
            self.cluster_file
        )

        questions = self.load_json(
            self.question_file
        )

        sources = self.load_json(
            self.source_file
        )


        graph = {

            "system":
            "FREE BASICS AI MARKETING SYSTEM",

            "type":
            "entity_graph",

            "version":
            "3.0",

            "status":
            "ACTIVE",

            "rules":
            {
                "verified_data_only": True,
                "source_required": True,
                "no_fake_landingpages": True,
                "official_assets_only": True,
                "tracking_required": True,
                "compliance_required": True
            },


            "nodes":
            {

                "partners": [],
                "products": [],
                "categories": [],
                "topics": [],
                "questions": [],
                "articles": [],
                "landingpages": [],
                "affiliate_assets": [],
                "tracking_assets": [],
                "sources": []

            },


            "relationships": []

        }



        partners=set()
        categories=set()



        # PRODUCTS

        for p in products.get(
            "entities",
            []
        ):

            pid=p.get("product_id")
            partner=p.get("partner")
            category=p.get("category")


            graph["nodes"]["products"].append(
                {
                    "id": pid,
                    "name": p.get("name"),
                    "partner": partner,
                    "category": category
                }
            )


            if partner:

                partners.add(partner)

                graph["relationships"].append(
                    {
                        "from": partner,
                        "relation": "provides",
                        "to": pid
                    }
                )


            if category:

                categories.add(category)

                graph["relationships"].append(
                    {
                        "from": pid,
                        "relation": "belongs_to",
                        "to": category
                    }
                )



        # PARTNERS

        for p in partners:

            graph["nodes"]["partners"].append(
                {
                    "id": p,
                    "type": "Partner"
                }
            )



        # CATEGORIES

        for c in categories:

            graph["nodes"]["categories"].append(
                {
                    "id": c,
                    "type": "Category"
                }
            )



        # ARTICLES

        for article in articles.get(
            "articles",
            []
        ):

            graph["nodes"]["articles"].append(
                article
            )


            graph["relationships"].append(
                {
                    "from": article.get("product_id"),
                    "relation": "has_content",
                    "to": article.get("article_id")
                }
            )



        # QUESTIONS

        for q in questions.get(
            "questions",
            []
        ):

            graph["nodes"]["questions"].append(
                q
            )

            graph["relationships"].append(
                {
                    "from": q.get("product_id"),
                    "relation": "answers",
                    "to": q.get("question_id")
                }
            )



        # TOPICS

        for c in clusters.get(
            "clusters",
            []
        ):

            graph["nodes"]["topics"].append(
                {
                    "id": c.get("cluster"),
                    "type": "SemanticCluster"
                }
            )



        # LANDINGPAGES

        if self.landingpage_folder.exists():

            for file in self.landingpage_folder.glob("*.html"):

                if file.name != "affiliate_html_status.json":

                    pid=file.stem

                    graph["nodes"]["landingpages"].append(
                        {
                            "id": pid,
                            "file": str(file),
                            "type": "LandingPage"
                        }
                    )


                    graph["relationships"].append(
                        {
                            "from": pid,
                            "relation": "represented_by",
                            "to": pid
                        }
                    )



        # AFFILIATE ASSETS

        for asset in assets_graph.get(
            "assets",
            []
        ):

            graph["nodes"]["affiliate_assets"].append(
                asset
            )


            if asset.get("asset_id"):

                graph["relationships"].append(
                    {
                        "from": asset.get("product_name"),
                        "relation": "has_official_asset",
                        "to": asset.get("asset_id")
                    }
                )



        # PRIMARY TRACKING ASSETS

        for pid,item in primary_assets.get(
            "products",
            {}
        ).items():

            asset=item.get(
                "primary_asset",
                {}
            )


            if asset:

                graph["nodes"]["tracking_assets"].append(
                    {
                        "id": asset.get("asset_id"),
                        "source": asset.get("source")
                    }
                )


                graph["relationships"].append(
                    {
                        "from": pid,
                        "relation": "uses_primary_asset",
                        "to": asset.get("asset_id")
                    }
                )



        # SOURCES

        for s in sources.get(
            "connections",
            {}
        ).get(
            "product_to_source",
            []
        ):

            graph["nodes"]["sources"].append(
                {
                    "id": s.get("source")
                }
            )

            graph["relationships"].append(
                {
                    "from": s.get("product_id"),
                    "relation": "supported_by",
                    "to": s.get("source")
                }
            )



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



        print("ENTITY GRAPH V3 CREATED")

        for k,v in graph["nodes"].items():

            print(
                k,
                ":",
                len(v)
            )


        print(
            "RELATIONSHIPS:",
            len(graph["relationships"])
        )



if __name__ == "__main__":

    EntityGraphPopulationBuilder().build()
