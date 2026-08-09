import json
from pathlib import Path


class NavigationIntelligenceBuilder:


    def __init__(self):

        self.entity_file = Path(
            "data_master/knowledge_master/entity_layer/entity_graph.json"
        )

        self.topic_file = Path(
            "data_master/content_intelligence/semantic_cluster_graph.json"
        )

        self.silo_file = Path(
            "data_master/linking/silo_structure.json"
        )

        self.output = Path(
            "data_master/content_intelligence/navigation_intelligence_graph.json"
        )


    def load(self,path):

        if not path.exists():

            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def find_silo(self,product_id,topic_map):


        return topic_map.get(
            product_id,
            "allgemein"
        )



    def build(self):


        entity = self.load(
            self.entity_file
        )

        topic = self.load(
            self.topic_file
        )

        silo = self.load(
            self.silo_file
        )



        graph = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "navigation_intelligence_graph",


            "version":
            "3.0",


            "status":
            "ACTIVE",


            "rules":
            {

                "master_entity_source":
                True,

                "semantic_navigation":
                True,

                "footer_connected":
                True,

                "no_random_links":
                True

            },


            "navigation":
            {

                "root":
                [
                    {
                        "name":
                        "Free Basics",

                        "url":
                        "/"
                    }
                ],

                "silos": [],

                "hubs": [],

                "categories": [],

                "footer": [],

                "related_content": []

            },


            "connections":
            {

                "product_to_silo": [],

                "product_to_footer": [],

                "product_to_category": [],

                "product_to_topic": [],

                "content_to_related": []

            }

        }



        # Topic Mapping

        topic_map={}


        for item in topic.get(
            "connections",
            {}
        ).get(
            "topic_to_product",
            []
        ):

            topic_map[
                item.get("product_id")
            ] = item.get("topic")





        # Product Master

        products = entity.get(
            "nodes",
            {}
        ).get(
            "products",
            []
        )



        silos=set()
        categories=set()



        for product in products:


            pid = product.get(
                "id"
            )

            category = product.get(
                "category"
            )


            topic_name = self.find_silo(
                pid,
                topic_map
            )


            silos.add(
                topic_name
            )


            if category:

                categories.add(
                    category
                )



            graph["connections"]["product_to_silo"].append(

                {

                    "product_id":
                    pid,

                    "silo":
                    topic_name

                }

            )


            graph["connections"]["product_to_footer"].append(

                {

                    "product_id":
                    pid,

                    "footer":
                    topic_name

                }

            )


            if category:

                graph["connections"]["product_to_category"].append(

                    {

                        "product_id":
                        pid,

                        "category":
                        category

                    }

                )


            if topic_name:


                graph["connections"]["product_to_topic"].append(

                    {

                        "product_id":
                        pid,

                        "topic":
                        topic_name

                    }

                )


            graph["navigation"]["related_content"].append(

                {

                    "product_id":
                    pid,

                    "category":
                    category,

                    "topic":
                    topic_name

                }

            )





        # Silo Navigation


        for s in sorted(silos):


            graph["navigation"]["silos"].append(

                {

                    "id":
                    s,

                    "type":
                    "semantic_silo"

                }

            )



            graph["navigation"]["hubs"].append(

                {

                    "silo":
                    s,

                    "url":
                    "/"+s

                }

            )


            graph["navigation"]["footer"].append(

                {

                    "section":
                    s,

                    "type":
                    "footer_navigation"

                }

            )





        for c in sorted(categories):

            graph["navigation"]["categories"].append(

                {

                    "category":
                    c

                }

            )





        self.output.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.output,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(

                graph,

                f,

                indent=2,

                ensure_ascii=False

            )



        print(
            "NAVIGATION INTELLIGENCE GRAPH V3 CREATED"
        )


        for k,v in graph["connections"].items():

            print(
                k,
                ":",
                len(v)
            )





if __name__=="__main__":

    NavigationIntelligenceBuilder().build()
