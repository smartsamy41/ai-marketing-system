import json
from pathlib import Path


class ContentGapBuilder:


    def __init__(self):

        self.cluster_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.question_file = Path(
            "data_master/content_intelligence/question_intelligence_graph.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/content_gap_analysis.json"
        )



    def load(self, path):

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def build(self):


        clusters = self.load(
            self.cluster_file
        )

        questions = self.load(
            self.question_file
        )

        articles = self.load(
            self.article_file
        )



        question_products = set()


        for item in questions.get(
            "questions",
            []
        ):

            question_products.add(

                item.get(
                    "product_id"
                )

            )



        article_products = set()


        for item in articles.get(
            "articles",
            []
        ):

            article_products.add(

                item.get(
                    "product_id"
                )

            )



        report = {


            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "content_gap_analysis",


            "version":
                "1.0",


            "status":
                "ACTIVE",



            "rules":
            {

                "no_fake_content":
                    True,

                "source_based":
                    True,

                "missing_content_detection_only":
                    True

            },


            "clusters": [],


            "gaps": []

        }



        for cluster in clusters.get(
            "clusters",
            []
        ):


            cluster_name = cluster.get(
                "cluster",
                ""
            )


            products = cluster.get(
                "products",
                []
            )


            cluster_result = {


                "cluster":
                    cluster_name,


                "products":
                    len(products),


                "questions":
                    0,


                "articles":
                    0,


                "missing_questions": [],


                "missing_articles": []


            }



            for product_id in products:


                if product_id in question_products:

                    cluster_result["questions"] += 1

                else:

                    cluster_result["missing_questions"].append(

                        product_id

                    )



                if product_id in article_products:

                    cluster_result["articles"] += 1

                else:

                    cluster_result["missing_articles"].append(

                        product_id

                    )



            report["clusters"].append(

                cluster_result

            )



            if cluster_result["missing_questions"]:


                report["gaps"].append(

                    {

                        "type":
                            "QUESTION_GAP",

                        "cluster":
                            cluster_name,

                        "products":
                            cluster_result["missing_questions"]

                    }

                )



            if cluster_result["missing_articles"]:


                report["gaps"].append(

                    {

                        "type":
                            "ARTICLE_GAP",

                        "cluster":
                            cluster_name,

                        "products":
                            cluster_result["missing_articles"]

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

                report,

                f,

                indent=2,

                ensure_ascii=False

            )



        print(
            "CONTENT GAP ANALYSIS CREATED"
        )


        print(
            "CLUSTERS:",
            len(report["clusters"])
        )


        print(
            "GAPS:",
            len(report["gaps"])
        )


        return report





if __name__ == "__main__":


    builder = ContentGapBuilder()

    builder.build()
