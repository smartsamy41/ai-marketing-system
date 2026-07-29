import json
from pathlib import Path

from engine.knowledge_adapter import KnowledgeAdapter
from engine.url_management.url_resolver import URLResolver
from engine.content_generation.landingpage_builder import LandingPageBuilder
from engine.content_generation.blog_article_builder import BlogArticleBuilder


class ContentPipeline:


    def __init__(self):

        self.knowledge = KnowledgeAdapter()

        self.urls = URLResolver()

        self.landingpage_builder = LandingPageBuilder()

        self.article_builder = BlogArticleBuilder()

        self.catalog_file = Path(
            "data_master/catalog/product_master_44.json"
        )



    def load_catalog(self):

        if not self.catalog_file.exists():

            return []


        data = json.loads(
            self.catalog_file.read_text(
                encoding="utf-8"
            )
        )


        return data.get(
            "products",
            []
        )



    def get_related_products(
        self,
        product
    ):

        catalog = self.load_catalog()


        current_id = product.get(
            "product_id"
        )


        current_category = product.get(
            "category",
            ""
        ).lower()


        related = []


        for item in catalog:


            if item.get(
                "product_id"
            ) == current_id:

                continue



            item_category = item.get(
                "category",
                ""
            ).lower()



            if item_category == current_category:

                related.append(
                    {
                        "product_id":
                            item.get(
                                "product_id"
                            ),

                        "category":
                            item.get(
                                "category"
                            )
                    }
                )



        return related[:8]



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



        landingpage = self.landingpage_builder.build(

            product,

            facts=knowledge_data

        )



        landingpage_html = self.landingpage_builder.render(
            landingpage
        )



        related_products = self.get_related_products(
            product
        )



        article = self.article_builder.build(

            product,

            facts=knowledge_data,

            related_products=related_products

        )



        article_html = self.article_builder.render(
            article
        )



        return {


            "product":
                product,


            "related_products":
                related_products,


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
