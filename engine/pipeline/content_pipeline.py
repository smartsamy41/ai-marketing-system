from engine.knowledge_adapter import KnowledgeAdapter
from engine.url_management.url_resolver import URLResolver
from engine.content_generation.landingpage_builder import LandingpageBuilder
from engine.content_generation.blog_article_builder import BlogArticleBuilder


class ContentPipeline:


    def __init__(self):

        self.knowledge = KnowledgeAdapter()

        self.urls = URLResolver()

        self.landingpage_builder = LandingpageBuilder()

        self.article_builder = BlogArticleBuilder()



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



        # Master Daten + Knowledge Layer verbinden

        product.update(
            knowledge_data
        )



        # Produktions URLs

        product["landingpage_url"] = (
            self.urls.landingpage_url(product)
        )


        product["article_url"] = (
            self.urls.article_url(product)
        )



        # Sicherheitsfelder

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
            "key_facts",
            []
        )


        product.setdefault(
            "comparison_matrix",
            []
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


        product.setdefault(
            "updated_at",
            ""
        )



        # NEU:
        # echte LandingpageBuilder Ausgabe

        landingpage = self.landingpage_builder.build(

            product,

            facts=knowledge_data,

            sources=product.get(
                "sources",
                []
            )

        )



        # Blog Artikel erstellen

        landingpage_html = self.landingpage_builder.render(
            landingpage
        )


        article = self.article_builder.build(

            product,

            facts=knowledge_data

        )



        article.update(

            {

                "summary":
                    product.get(
                        "summary",
                        ""
                    ),


                "sources":
                    product.get(
                        "sources",
                        []
                    ),


                "author":
                    product.get(
                        "author"
                    ),


                "reviewed_by":
                    product.get(
                        "reviewed_by"
                    ),


                "updated_at":
                    product.get(
                        "updated_at"
                    )

            }

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


            "status":
                "READY"


        }





if __name__ == "__main__":


    import json


    pipeline = ContentPipeline()


    result = pipeline.process(

        {

            "product_id":
                "CHK24_001",

            "name":
                "Strom",

            "partner":
                "check24",

            "category":
                "Strom"

        }

    )


    print(

        json.dumps(

            result,

            indent=2,

            ensure_ascii=False

        )

    )
