from engine.pipeline.content_pipeline import ContentPipeline
from engine.content_production_bridge import ContentProductionBridge


class ContentPipelineAdapter:


    def __init__(self):

        self.pipeline = ContentPipeline()

        self.production = ContentProductionBridge()



    def generate(
        self,
        product
    ):


        pipeline_result = self.pipeline.process(
            product
        )


        if pipeline_result.get("status") != "READY":

            return {

                "title": "",

                "seo_title": "",

                "description": "",

                "body": "",

                "faq": [],

                "status": "ERROR",

                "reason":
                    pipeline_result.get(
                        "message",
                        "Pipeline failed"
                    )

            }



        publish_result = self.production.publish(
            pipeline_result
        )


        article = pipeline_result.get(
            "article",
            {}
        )


        landingpage = pipeline_result.get(
            "landingpage",
            {}
        )



        return {


            "title":
                article.get(
                    "title",
                    ""
                ),



            "seo_title":
                article.get(
                    "title",
                    ""
                ),



            "description":
                article.get(
                    "description",
                    ""
                ),



            "body":
                article.get(
                    "content",
                    ""
                ),



            "faq":
                article.get(
                    "faq",
                    []
                ),



            "landingpage":
                landingpage,



            "article":
                article,



            "publish_result":
                publish_result,



            "status":
                "generated"

        }
