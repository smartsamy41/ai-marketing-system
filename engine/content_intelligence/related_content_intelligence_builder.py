import json
from pathlib import Path


class RelatedContentIntelligenceBuilder:


    def __init__(self):

        self.article_graph = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.question_graph = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.internal_graph = Path(
            "data_master/content_intelligence/internal_link_graph.json"
        )

        self.navigation_graph = Path(
            "data_master/content_intelligence/navigation_intelligence_graph.json"
        )

        self.output = Path(
            "data_master/content_intelligence/related_content_intelligence_graph.json"
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


        article = self.load(
            self.article_graph
        )

        question = self.load(
            self.question_graph
        )

        internal = self.load(
            self.internal_graph
        )

        navigation = self.load(
            self.navigation_graph
        )



        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "related_content_intelligence_graph",


            "version":
            "1.0",


            "status":
            "ACTIVE",


            "rules":
            {

                "generated_from_entities":
                True,

                "no_old_content_copy":
                True,

                "semantic_relationships_only":
                True,

                "source_based":
                True

            },


            "connections":
            {

                "article_to_related_article": [],

                "article_to_related_question": [],

                "article_to_related_product": [],

                "article_to_related_topic": [],

                "article_to_related_landingpage": [],

                "product_to_related_content": []

            }

        }



        # Artikel Beziehungen aus interner Struktur


        for item in internal.get(
            "connections",
            {}
        ).get(
            "article_to_article",
            []
        ):


            graph["connections"]["article_to_related_article"].append(
                item
            )



        for item in internal.get(
            "connections",
            {}
        ).get(
            "article_to_question",
            []
        ):


            graph["connections"]["article_to_related_question"].append(
                item
            )



        # Produkt / Topic / Landingpage Verbindungen


        for item in article.get(
            "connections",
            {}
        ).get(
            "article_to_product",
            []
        ):


            graph["connections"]["article_to_related_product"].append(
                item
            )



        for item in article.get(
            "connections",
            {}
        ).get(
            "article_to_topic",
            []
        ):


            graph["connections"]["article_to_related_topic"].append(
                item
            )



        for item in article.get(
            "connections",
            {}
        ).get(
            "article_to_landingpage",
            []
        ):


            graph["connections"]["article_to_related_landingpage"].append(
                item
            )



        # Produkt Navigation Verbindung


        for item in navigation.get(
            "connections",
            {}
        ).get(
            "product_to_footer",
            []
        ):


            graph["connections"]["product_to_related_content"].append(
                item
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
            "RELATED CONTENT INTELLIGENCE GRAPH CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )





if __name__ == "__main__":

    RelatedContentIntelligenceBuilder().build()
