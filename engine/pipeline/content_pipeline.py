import json
from pathlib import Path

from engine.knowledge_adapter import KnowledgeAdapter
from engine.url_management.url_resolver import URLResolver
from engine.content_generation.landingpage_builder import LandingPageBuilder
from engine.content_generation.blog_article_builder import BlogArticleBuilder
from engine.self_learning_agent.product_relationship_resolver import ProductRelationshipResolver


class ContentPipeline:


    def __init__(self):

        self.knowledge = KnowledgeAdapter()

        self.urls = URLResolver()

        self.landingpage_builder = LandingPageBuilder()

        self.article_builder = BlogArticleBuilder()

        self.relationship_resolver = ProductRelationshipResolver()



    def process(
        self,
        product
    ):


        knowledge_data = self.knowledge.build_product_context(
            product["product_id"]
        )


        if not knowledge_data:

            return {

                "status":
                    "ERROR",

                "message":
                    "Product not found"

            }



        product.update(
            knowledge_data
        )



        product["landingpage_url"] = (
            self.urls.landingpage_url(
                product
            )
        )


        product["article_url"] = (
            self.urls.article_url(
                product
            )
        )



        product.setdefault(
            "hero_title",
            product.get(
                "name",
                ""
            )
        )


        product.setdefault(
            "summary",
            ""
        )


        product.setdefault(
            "faq",
            []
        )


        product.setdefault(
            "sources",
            []
        )


        product.setdefault(
            "author",
            "Redaktion Free Basics"
        )


        product.setdefault(
            "reviewed_by",
            "Samy ben Chedli Jendoubi"
        )



        relationship_data = (
            self.relationship_resolver.resolve(
                product
            )
        )



        product.update(
            {

                "related_products":
                    relationship_data.get(
                        "related_products",
                        []
                    ),

                "newsletter_segment":
                    relationship_data.get(
                        "newsletter_segment",
                        ""
                    ),

                "product_type":
                    relationship_data.get(
                        "type",
                        ""
                    )

            }
        )



        landingpage = self.landingpage_builder.build(

            product,

            facts=knowledge_data

        )


        landingpage_html = self.landingpage_builder.render(
            landingpage
        )



        article = self.article_builder.build(

            product,

            facts=knowledge_data,

            related_products=product.get(
                "related_products",
                []
            )

        )


        article.update(

            {

                "newsletter_segment":
                    product.get(
                        "newsletter_segment",
                        ""
                    ),

                "product_type":
                    product.get(
                        "product_type",
                        ""
                    )

            }

        )



        article_html = self.article_builder.render(
            article
        )



        return {


            "product":
                product,


            "relationship":
                relationship_data,


            "landingpage":
                landingpage,


            "landingpage_html":
                landingpage_html,


            "article":
                article,


            "article_html":
                article_html,


            "status":
                "READY"

        }




if __name__ == "__main__":


    pipeline = ContentPipeline()


    result = pipeline.process(

        {

            "product_id":
                "CHK24_001",

            "name":
                "Strom",

            "category":
                "Strom",

            "partner":
                "check24"

        }

    )


    print(

        json.dumps(

            result,

            indent=2,

            ensure_ascii=False

        )

    )
