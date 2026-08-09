import json
from pathlib import Path
from datetime import datetime, timezone


class SchemaRenderer:

    def __init__(self):

        self.page_source = Path(
            "data_master/content_production/rendered_page_architecture.json"
        )

        self.entity_source = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.output = Path(
            "data_master/content_production/schema_output"
        )


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def load_entities(self):

        data = self.load_json(
            self.entity_source
        )

        result = {}

        for entity in data.get(
            "entities",
            []
        ):

            result[
                entity.get("product_id")
            ] = entity


        return result



    def create_schema(
        self,
        page,
        entity
    ):


        product_id = page.get(
            "product_id",
            ""
        )


        article_id = page.get(
            "article_id",
            ""
        )


        schema = [

            {

                "@context":
                "https://schema.org",

                "@type":
                "Organization",

                "name":
                "Free Basics"

            },


            {

                "@context":
                "https://schema.org",

                "@type":
                "WebSite",

                "name":
                "Free Basics",

                "url":
                "https://freebasics.online"

            },


            {

                "@context":
                "https://schema.org",

                "@type":
                "Product",

                "identifier":
                product_id,

                "name":
                entity.get(
                    "name",
                    product_id
                ),

                "category":
                entity.get(
                    "category",
                    ""
                ),

                "brand":
                {

                    "@type":
                    "Organization",

                    "name":
                    "Free Basics"

                }

            },


            {

                "@context":
                "https://schema.org",

                "@type":
                "Article",

                "identifier":
                article_id,

                "about":
                {

                    "@type":
                    "Product",

                    "identifier":
                    product_id

                }

            },


            {

                "@context":
                "https://schema.org",

                "@type":
                "BreadcrumbList",

                "itemListElement":

                [

                    {

                        "@type":
                        "ListItem",

                        "position":
                        1,

                        "name":
                        "Free Basics"

                    },


                    {

                        "@type":
                        "ListItem",

                        "position":
                        2,

                        "name":
                        entity.get(
                            "name",
                            product_id
                        )

                    }

                ]

            },


            {

                "@context":
                "https://schema.org",

                "@type":
                "FAQPage",

                "mainEntity":
                []

            }

        ]


        return schema



    def build(self):


        pages_data = self.load_json(
            self.page_source
        )


        entities = self.load_entities()


        pages = pages_data.get(
            "pages",
            []
        )


        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        created = 0


        for page in pages:


            product_id = page.get(
                "product_id"
            )


            if not product_id:
                continue


            entity = entities.get(
                product_id,
                {}
            )


            schema = self.create_schema(
                page,
                entity
            )


            file = (
                self.output /
                f"{product_id}.json"
            )


            with open(
                file,
                "w",
                encoding="utf-8"
            ) as f:


                json.dump(
                    schema,
                    f,
                    indent=2,
                    ensure_ascii=False
                )


            created += 1



        print(
            "SCHEMA V2 CREATED"
        )

        print(
            "FILES:",
            created
        )

        print(
            "TIME:",
            datetime.now(
                timezone.utc
            ).isoformat()
        )



if __name__ == "__main__":

    SchemaRenderer().build()
