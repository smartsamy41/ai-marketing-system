import json
from pathlib import Path
from datetime import datetime, timezone


class OpenGraphRenderer:

    def __init__(self):

        self.page_source = Path(
            "data_master/content_production/rendered_page_architecture.json"
        )

        self.entity_source = Path(
            "data_master/knowledge_master/entity_layer/product_entities.json"
        )

        self.output = Path(
            "data_master/content_production/opengraph_output"
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

        entities = {}

        for entity in data.get(
            "entities",
            []
        ):

            entities[
                entity.get("product_id")
            ] = entity


        return entities



    def create_opengraph(
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


        name = entity.get(
            "name",
            product_id
        )


        category = entity.get(
            "category",
            ""
        )


        partner = entity.get(
            "partner",
            ""
        )


        url = (
            "https://freebasics.online/"
            + product_id
        )


        data = {


            "open_graph":

            {

                "og:title":
                f"{name} | Free Basics",


                "og:description":
                f"Informationen zu {name} aus dem Free Basics Produktsystem.",


                "og:type":
                "article",


                "og:url":
                url,


                "og:site_name":
                "Free Basics"

            },


            "twitter_card":

            {

                "twitter:card":
                "summary_large_image",


                "twitter:title":
                f"{name} | Free Basics",


                "twitter:description":
                f"Informationen zu {name}.",


                "twitter:url":
                url

            },


            "entity":

            {

                "product_id":
                product_id,


                "article_id":
                article_id,


                "name":
                name,


                "category":
                category,


                "partner":
                partner

            }

        }


        return data



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


            og = self.create_opengraph(
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
                    og,
                    f,
                    indent=2,
                    ensure_ascii=False
                )


            created += 1



        print(
            "OPENGRAPH V2 CREATED"
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

    OpenGraphRenderer().build()
