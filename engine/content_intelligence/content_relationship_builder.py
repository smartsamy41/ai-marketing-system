import json
from pathlib import Path
from datetime import datetime, timezone


class ContentRelationshipBuilder:

    def __init__(self):

        self.entity_topic_file = Path(
            "data_master/content_graph/entity_topic_graph.json"
        )

        self.catalog_file = Path(
            "data_master/catalog/product_master_44.json"
        )

        self.category_file = Path(
            "data_master/linking/category_map.json"
        )

        self.silo_file = Path(
            "data_master/linking/silo_structure.json"
        )

        self.newsletter_file = Path(
            "data_master/newsletter_layer/newsletter_product_mapping.json"
        )

        self.output_file = Path(
            "data_master/content_graph/content_relationships.json"
        )


    def load(self, file):

        if not file.exists():
            return {}

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)



    def build(self):

        entity_topic = self.load(
            self.entity_topic_file
        )

        catalog = self.load(
            self.catalog_file
        )

        categories = self.load(
            self.category_file
        ).get(
            "categories",
            {}
        )

        silos = self.load(
            self.silo_file
        ).get(
            "silos",
            {}
        )

        newsletter = self.load(
            self.newsletter_file
        )



        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "content_relationship_graph",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "rules":
                {
                    "validated_relationships_only": True,
                    "source_based_connections": True,
                    "no_random_links": True
                },


            "relationships":
                {

                    "product_to_partner": [],

                    "product_to_category": [],

                    "product_to_topic": [],

                    "product_to_article": [],

                    "product_to_landingpage": [],

                    "product_to_faq": [],

                    "product_to_location": [],

                    "article_to_question": [],

                    "article_to_source": [],

                    "article_to_entity": [],

                    "landingpage_to_article": [],

                    "newsletter_to_product": [],

                    "newsletter_to_content": []

                }

        }



        products = catalog.get(
            "products",
            []
        )


        #
        # PRODUCT RELATIONSHIPS
        #

        for product in products:

            product_id = product.get(
                "product_id"
            )


            partner = product.get(
                "partner",
                ""
            )


            category = product.get(
                "category",
                ""
            )


            if product_id:

                graph["relationships"]["product_to_partner"].append(

                    {
                        "product_id":
                            product_id,

                        "partner":
                            partner

                    }

                )


                graph["relationships"]["product_to_category"].append(

                    {
                        "product_id":
                            product_id,

                        "category":
                            category

                    }

                )



                #
                # Content URLs
                #

                graph["relationships"]["product_to_landingpage"].append(

                    {
                        "product_id":
                            product_id,

                        "landingpage":
                            product.get(
                                "landingpage",
                                ""
                            )

                    }

                )



        #
        # ENTITY -> TOPIC
        #

        for relation in entity_topic.get(
            "relationships",
            {}
        ).get(
            "entity_to_topic",
            []
        ):


            graph["relationships"]["product_to_topic"].append(

                {
                    "product_id":
                        relation.get(
                            "entity"
                        ),

                    "topic":
                        relation.get(
                            "topic"
                        )

                }

            )



        #
        # CATEGORY -> ARTICLE
        #

        for category,data in categories.items():

            product_id = data.get(
                "product_id"
            )


            article = data.get(
                "article",
                ""
            )


            if product_id and article:

                graph["relationships"]["product_to_article"].append(

                    {
                        "product_id":
                            product_id,

                        "article":
                            article

                    }

                )



        #
        # SILO -> RELATED PRODUCTS
        #

        for silo_name,silo in silos.items():

            for product_id in silo.get(
                "products",
                []
            ):

                graph["relationships"]["product_to_topic"].append(

                    {
                        "product_id":
                            product_id,

                        "silo":
                            silo_name

                    }

                )



        #
        # NEWSLETTER CONNECTION
        #

        for item in newsletter.get(
            "mappings",
            []
        ):

            graph["relationships"]["newsletter_to_product"].append(
                item
            )



        #
        # WRITE
        #

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
                graph,
                f,
                indent=2,
                ensure_ascii=False
            )


        return graph



if __name__ == "__main__":


    builder = ContentRelationshipBuilder()


    result = builder.build()


    print(
        "CONTENT RELATIONSHIP GRAPH CREATED"
    )


    for key,value in result["relationships"].items():

        print(
            key,
            ":",
            len(value)
        )
