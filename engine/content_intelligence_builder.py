import json
from pathlib import Path
from datetime import datetime, timezone


class ContentIntelligenceBuilder:

    def __init__(self):

        self.base = Path("data_master")

        self.catalog_file = (
            self.base /
            "catalog" /
            "product_master_44.json"
        )

        self.knowledge_file = (
            self.base /
            "knowledge_master" /
            "product_knowledge_master.json"
        )

        self.entity_file = (
            self.base /
            "geo_and_entities" /
            "entity_registry" /
            "entity_relationships.json"
        )

        self.category_file = (
            self.base /
            "linking" /
            "category_map.json"
        )

        self.silo_file = (
            self.base /
            "linking" /
            "silo_structure.json"
        )


        self.output_nodes = (
            self.base /
            "content_graph" /
            "content_nodes.json"
        )

        self.output_relationships = (
            self.base /
            "content_graph" /
            "content_relationships.json"
        )

        self.output_entity_topic = (
            self.base /
            "content_graph" /
            "entity_topic_graph.json"
        )

        self.output_intent = (
            self.base /
            "content_graph" /
            "search_intent_graph.json"
        )

        self.output_clusters = (
            self.base /
            "content_intelligence" /
            "topic_cluster_registry.json"
        )

        self.output_questions = (
            self.base /
            "content_intelligence" /
            "question_graph.json"
        )

        self.output_topics = (
            self.base /
            "knowledge_master" /
            "topic_layer" /
            "topic_registry.json"
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



    def save(
        self,
        file,
        data
    ):

        file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )



    def build(self):

        catalog = self.load(
            self.catalog_file
        )

        knowledge = self.load(
            self.knowledge_file
        )

        entities = self.load(
            self.entity_file
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



        nodes = {

            "products": [],
            "partners": [],
            "categories": [],
            "topics": [],
            "questions": [],
            "articles": [],
            "landingpages": [],
            "faq": [],
            "locations": [],
            "newsletters": [],
            "sources": []

        }



        relationships = {

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



        entity_topic = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "entity_topic_graph",

            "status":
                "ACTIVE",

            "entities": [],

            "topics": [],

            "relationships": {

                "entity_to_topic": [],
                "topic_to_question": [],
                "topic_to_article": [],
                "topic_to_product": [],
                "entity_to_source": [],
                "entity_to_geo": []

            }

        }



        topic_registry = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "topic_registry",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules": {

                "source_required": True,
                "verified_topics_only": True,
                "no_fabricated_topics": True

            },

            "topics": []

        }



        clusters = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "topic_cluster_registry",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "clusters": []

        }



        intents = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "search_intent_graph",

            "status":
                "ACTIVE",

            "intent_types": {

                "informational": [],
                "commercial": [],
                "transactional": [],
                "navigational": []

            },

            "mapping": {

                "question_to_topic": [],
                "topic_to_product": [],
                "topic_to_article": [],
                "intent_to_landingpage": [],
                "intent_to_geo": []

            }

        }



        questions = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "question_graph",

            "status":
                "ACTIVE",

            "rules": {

                "source_required": True,
                "intent_required": True,
                "no_fake_search_questions": True,
                "entity_connection_required": True

            },

            "intents": {

                "informational": [],
                "commercial": [],
                "transactional": [],
                "navigational": []

            },

            "questions": []

        }



        partners_seen = set()
        categories_seen = set()



        for product in catalog.get(
            "products",
            []
        ):


            product_id = product.get(
                "product_id"
            )


            name = product.get(
                "name",
                ""
            )


            category = product.get(
                "category",
                ""
            )


            partner = product.get(
                "partner",
                ""
            )


            if not product_id:

                continue



            nodes["products"].append(

                {
                    "product_id": product_id,
                    "name": name,
                    "category": category,
                    "partner": partner
                }

            )



            if partner and partner not in partners_seen:

                nodes["partners"].append(

                    {
                        "name": partner
                    }

                )

                partners_seen.add(
                    partner
                )



            if category and category not in categories_seen:

                nodes["categories"].append(

                    {
                        "name": category
                    }

                )

                categories_seen.add(
                    category
                )



            relationships["product_to_partner"].append(

                {
                    "product_id": product_id,
                    "partner": partner
                }

            )



            relationships["product_to_category"].append(

                {
                    "product_id": product_id,
                    "category": category
                }

            )



            category_key = category.lower()


            silo = ""

            for key,data in categories.items():

                if (
                    data.get("product_id") == product_id
                    or product_id in data.get("product_ids",[])
                ):

                    silo = data.get(
                        "silo",
                        ""
                    )

                    category_key = key

                    break



            if silo:


                nodes["topics"].append(

                    {
                        "topic": silo,
                        "product_id": product_id
                    }

                )


                topic_registry["topics"].append(

                    {
                        "topic": silo,
                        "product_id": product_id,
                        "source": "category_map"
                    }

                )


                clusters["clusters"].append(

                    {
                        "cluster": silo,
                        "product_id": product_id,
                        "category": category_key
                    }

                )


                relationships["product_to_topic"].append(

                    {
                        "product_id": product_id,
                        "topic": silo
                    }

                )


                entity_topic["relationships"]["topic_to_product"].append(

                    {
                        "topic": silo,
                        "product_id": product_id
                    }

                )



            relationships["product_to_article"].append(

                {
                    "product_id": product_id,
                    "article": f"/blog/{product_id.lower()}-ratgeber"
                }

            )


            relationships["product_to_landingpage"].append(

                {
                    "product_id": product_id,
                    "landingpage": f"/lp/{product_id}"
                }

            )



        for item in entities.get(
            "relationships",
            []
        ):

            entity_topic["entities"].append(

                {
                    "entity": item.get("to_entity"),
                    "source": item.get("source")
                }

            )



        timestamp = datetime.now(
            timezone.utc
        ).isoformat()



        nodes["generated_at"] = timestamp


        self.save(
            self.output_nodes,
            {
                "system":
                    "FREE BASICS AI MARKETING SYSTEM",
                "type":
                    "content_graph_nodes",
                "version":
                    "1.0",
                "status":
                    "ACTIVE",
                "nodes":
                    nodes
            }
        )


        self.save(
            self.output_relationships,
            {
                "system":
                    "FREE BASICS AI MARKETING SYSTEM",
                "type":
                    "content_relationship_graph",
                "status":
                    "ACTIVE",
                "relationships":
                    relationships
            }
        )


        self.save(
            self.output_entity_topic,
            entity_topic
        )


        self.save(
            self.output_intent,
            intents
        )


        self.save(
            self.output_clusters,
            clusters
        )


        self.save(
            self.output_questions,
            questions
        )


        self.save(
            self.output_topics,
            topic_registry
        )



        return {

            "status":
                "READY",

            "products":
                len(nodes["products"]),

            "topics":
                len(topic_registry["topics"]),

            "clusters":
                len(clusters["clusters"])

        }



if __name__ == "__main__":


    builder = ContentIntelligenceBuilder()


    result = builder.build()


    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
