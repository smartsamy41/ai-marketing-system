import json
from pathlib import Path


class SchemaGraphBuilder:


    def __init__(self):

        self.entity_file = Path(
            "data_master/geo_and_entities/entity_registry/organization_profile.json"
        )

        self.product_registry = Path(
            "data_master/geo_and_entities/entity_registry/product_facts_registry.json"
        )



    def load_json(self, file):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def load_entity(self):

        return self.load_json(
            self.entity_file
        )



    def load_product_registry(self):

        return self.load_json(
            self.product_registry
        )



    def find_product_entity(
        self,
        product_id
    ):

        registry = self.load_product_registry()


        for product in registry.get(
            "products",
            []
        ):

            if product.get(
                "product_id"
            ) == product_id:

                return product


        return {}



    def organization_schema(self):

        entity = self.load_entity()


        return {

            "@context":
                "https://schema.org",

            "@type":
                "Organization",

            "@id":
                entity["domain"] + "/#organization",

            "name":
                entity["name"],

            "url":
                entity["domain"]

        }



    def product_schema(
        self,
        product
    ):

        product_id = (
            product.get("product_id")
            or ""
        )


        entity = self.find_product_entity(
            product_id
        )


        name = (
            product.get("name")
            or entity.get("name")
            or ""
        )


        category = (
            product.get("category")
            or entity.get("category")
            or ""
        )


        partner = (
            product.get("partner")
            or entity.get("partner")
            or ""
        )


        schema = {

            "@context":
                "https://schema.org",

            "@type":
                "Product",

            "@id":
                f"https://freebasics.online/#{product_id}",

            "name":
                name,

            "category":
                category,

            "productID":
                product_id,


            "brand":
                {

                    "@type":
                        "Organization",

                    "name":
                        partner

                },


            "isPartOf":
                {

                    "@type":
                        "WebSite",

                    "name":
                        "Free Basics",

                    "url":
                        "https://freebasics.online"

                }

        }



        kg = entity.get(
            "knowledge_graph",
            {}
        )


        same_as = []


        if kg.get(
            "wikidata_id"
        ):

            same_as.append(
                "https://www.wikidata.org/wiki/"
                +
                kg["wikidata_id"]
            )


        if same_as:

            schema["sameAs"] = same_as



        return schema



    def article_schema(
        self,
        article
    ):


        return {

            "@context":
                "https://schema.org",

            "@type":
                "Article",

            "headline":
                article.get(
                    "title"
                ),


            "url":
                article.get(
                    "article_url",
                    ""
                ),


            "mainEntityOfPage":
                {
                    "@type":
                        "WebPage",

                    "@id":
                        article.get(
                            "article_url",
                            ""
                        )
                },


            "description":
                article.get(
                    "description",
                    ""
                ),


            "datePublished":
                article.get(
                    "published_at",
                    article.get(
                        "updated_at",
                        ""
                    )
                ),


            "dateModified":
                article.get(
                    "updated_at",
                    ""
                ),

            "author":
                {

                    "@type":
                        "Organization",

                    "name":
                        "Free Basics Redaktion"

                }

        }



if __name__ == "__main__":


    builder = SchemaGraphBuilder()


    print(
        json.dumps(
            builder.product_schema(
                {
                    "product_id":"CHK24_001"
                }
            ),
            indent=2,
            ensure_ascii=False
        )
    )
