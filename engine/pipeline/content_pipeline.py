import json

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



    def normalize_slug(self, text):

        text = str(text).lower()

        replacements = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss"
        }

        for old, new in replacements.items():
            text = text.replace(old, new)


        remove_chars = [
            "/",
            "\\",
            "&",
            ",",
            ".",
            ":",
            ";",
            "(",
            ")"
        ]

        for char in remove_chars:
            text = text.replace(char, "-")


        parts = []

        for part in text.split("-"):

            if part.strip():

                parts.append(part.strip())


        return "-".join(parts)



    def process(
        self,
        product
    ):


        knowledge_data = self.knowledge.build_product_context(
            product["product_id"]
        )


        if not knowledge_data:

            return {

                "status": "ERROR",

                "message": "Product not found"

            }



        product.update(
            knowledge_data
        )


        product["summary"] = (

            knowledge_data.get(
                "summary"
            )

            or

            product.get(
                "summary",
                ""
            )

        )



        product["key_facts"] = (

            knowledge_data.get(
                "key_facts"
            )

            or

            knowledge_data.get(
                "facts"
            )

            or

            []

        )



        product["faq"] = (

            knowledge_data.get(
                "faq"
            )

            or

            []

        )



        product["sources"] = (

            knowledge_data.get(
                "sources"
            )

            or

            []

        )



        product["slug"] = self.normalize_slug(
            product.get(
                "name",
                ""
            )
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


                "silo":

                    relationship_data.get(
                        "silo",
                        ""
                    ),


                "cluster":

                    relationship_data.get(
                        "category",
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


        landingpage["html"] = landingpage_html



        article = self.article_builder.build(

            product,

            facts=knowledge_data,

            related_products=product.get(
                "related_products",
                []
            )

        )


        article["newsletter_segment"] = product.get(
            "newsletter_segment",
            ""
        )


        article["product_type"] = product.get(
            "product_type",
            ""
        )



        article_html = self.article_builder.render(
            article
        )



        return {


            "product":

                product,


            "landingpage":

                landingpage,


            "landingpage_html":

                landingpage_html,


            "article":

                article,


            "article_html":

                article_html,


            "relationship":

                relationship_data,


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
                "Energie",

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
