from engine.rendering.production_renderer import ProductionRenderer
from engine.publishing.repository_publisher import RepositoryPublisher
from urllib.parse import urlparse


class ContentProductionBridge:


    def __init__(self):

        self.renderer = ProductionRenderer()
        self.publisher = RepositoryPublisher()



    def publish(
        self,
        pipeline_result
    ):

        if pipeline_result.get("status") != "READY":

            return {
                "status": "ERROR",
                "message": "Pipeline result not ready"
            }



        product = pipeline_result.get(
            "product",
            {}
        )

        landingpage = pipeline_result.get(
            "landingpage",
            {}
        )

        article = pipeline_result.get(
            "article",
            {}
        )



        landingpage_html = self.renderer.render_landingpage(
            landingpage
        )


        article_html = self.renderer.render_article(
            article
        )



        product_id = str(
            product.get(
                "product_id",
                "unknown"
            )
        )



        landingpage_url = str(
            landingpage.get(
                "canonical_url",
                product.get(
                    "landingpage_url",
                    ""
                )
            )
        )



        landingpage_slug = (
            urlparse(
                landingpage_url
            )
            .path
            .rstrip("/")
            .split("/")[-1]
            or product_id
        )



        landingpage_path = self.publisher.save_landingpage(
            landingpage_slug,
            landingpage_html
        )



        article_slug = f"{landingpage_slug}-ratgeber"


        article_path = self.publisher.save_article(
            article_slug,
            article_html
        )



        return {

            "status": "PUBLISHED",

            "product_id":
                product_id,

            "landingpage":
                landingpage_path,

            "article":
                article_path

        }



if __name__ == "__main__":


    bridge = ContentProductionBridge()

    print(
        bridge.publish(
            {
                "status": "ERROR"
            }
        )
    )
