import json
from pathlib import Path


class AuthoritySourceGraphBuilder:


    def __init__(self):

        self.product_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
        )

        self.entity_file = Path(
            "data_master/geo_and_entities/entity_registry/entity_relationships.json"
        )

        self.source_file = Path(
            "data_master/source_layer/knowledge_sources.json"
        )

        self.primary_source_file = Path(
            "data_master/geo_and_entities/primary_sources_index.json"
        )

        self.backlink_file = Path(
            "data_master/authority_layer/backlink_registry.json"
        )

        self.article_file = Path(
            "data_master/content_graph/article_intelligence_graph.json"
        )

        self.output_file = Path(
            "data_master/content_intelligence/authority_source_graph.json"
        )


    def load(
        self,
        path
    ):

        if not path.exists():
            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    @staticmethod
    def clean(
        value
    ):

        if value is None:
            return ""

        return str(
            value
        ).strip()


    def build(self):


        products = self.load(
            self.product_file
        )

        entities = self.load(
            self.entity_file
        )

        sources = self.load(
            self.source_file
        )

        primary_sources = self.load(
            self.primary_source_file
        )

        backlinks = self.load(
            self.backlink_file
        )

        articles = self.load(
            self.article_file
        )


        graph = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "authority_source_graph",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "rules":
            {

                "verified_sources_only":
                    True,

                "source_required_for_claims":
                    True,

                "no_fabricated_sources":
                    True,

                "entity_source_relationship_required":
                    True,

                "verified_backlinks_only":
                    True,

                "backlink_must_be_active":
                    True,

                "backlink_must_be_link_verified":
                    True,

                "no_fabricated_authority_metrics":
                    True

            },

            "connections":
            {

                "product_to_source": [],

                "entity_to_source": [],

                "article_to_source": [],

                "partner_to_source": [],

                "verified_backlinks": []

            },

            "validation":
            {

                "products_checked":
                    0,

                "sources_found":
                    0,

                "backlinks_checked":
                    0,

                "verified_backlinks":
                    0,

                "backlink_domains":
                    0

            }

        }


        # =====================================================
        # SOURCE REGISTRY
        # =====================================================

        source_names = []


        for source in sources.get(
            "sources",
            []
        ):

            name = source.get(
                "name"
            )

            if name:

                source_names.append(
                    name
                )


        for source in primary_sources.get(
            "sources",
            []
        ):

            name = source.get(
                "name"
            )

            if name:

                source_names.append(
                    name
                )


        source_names = list(
            set(
                source_names
            )
        )


        graph[
            "validation"
        ][
            "sources_found"
        ] = len(
            source_names
        )


        # =====================================================
        # PRODUCT / PARTNER SOURCES
        # =====================================================

        for product in products.get(
            "products",
            []
        ):


            product_id = product.get(
                "product_id"
            )


            partner = product.get(
                "identity",
                {}
            ).get(
                "partner",
                ""
            )


            product_source = product.get(
                "knowledge",
                {}
            ).get(
                "llm_context",
                {}
            ).get(
                "source_reference",
                ""
            )


            if product_id:


                graph[
                    "validation"
                ][
                    "products_checked"
                ] += 1


                if product_source:


                    graph[
                        "connections"
                    ][
                        "product_to_source"
                    ].append(

                        {

                            "product_id":
                                product_id,

                            "source":
                                product_source

                        }

                    )


                elif partner:


                    graph[
                        "connections"
                    ][
                        "product_to_source"
                    ].append(

                        {

                            "product_id":
                                product_id,

                            "source":
                                partner

                        }

                    )


                if partner:


                    graph[
                        "connections"
                    ][
                        "partner_to_source"
                    ].append(

                        {

                            "partner":
                                partner,

                            "product_id":
                                product_id

                        }

                    )


        # =====================================================
        # ENTITY SOURCES
        # =====================================================

        for relationship in entities.get(
            "relationships",
            []
        ):


            entity = relationship.get(
                "to_entity"
            )


            source = relationship.get(
                "source"
            )


            if entity and source:


                graph[
                    "connections"
                ][
                    "entity_to_source"
                ].append(

                    {

                        "entity":
                            entity,

                        "source":
                            source

                    }

                )


        # =====================================================
        # ARTICLE SOURCES
        # =====================================================

        for article in articles.get(
            "articles",
            []
        ):


            product_id = article.get(
                "product_id"
            )


            for link in graph[
                "connections"
            ][
                "product_to_source"
            ]:


                if link.get(
                    "product_id"
                ) == product_id:


                    graph[
                        "connections"
                    ][
                        "article_to_source"
                    ].append(

                        {

                            "article_id":
                                article.get(
                                    "article_id"
                                ),

                            "source":
                                link.get(
                                    "source"
                                )

                        }

                    )


        # =====================================================
        # VERIFIED BACKLINKS
        # =====================================================

        backlink_domains = set()

        seen_backlinks = set()


        for backlink in backlinks.get(
            "backlinks",
            []
        ):


            graph[
                "validation"
            ][
                "backlinks_checked"
            ] += 1


            status = self.clean(
                backlink.get(
                    "status"
                )
            ).upper()


            link_verified = bool(
                backlink.get(
                    "link_verified",
                    False
                )
            )


            source_url = self.clean(
                backlink.get(
                    "source_url"
                )
            )


            source_domain = self.clean(
                backlink.get(
                    "source_domain"
                )
            )


            target_url = self.clean(
                backlink.get(
                    "target_url"
                )
            )


            if status != "ACTIVE":
                continue


            if not link_verified:
                continue


            if not source_url:
                continue


            if not source_domain:
                continue


            if not target_url:
                continue


            backlink_key = (
                source_url,
                target_url
            )


            if backlink_key in seen_backlinks:
                continue


            seen_backlinks.add(
                backlink_key
            )


            backlink_domains.add(
                source_domain
            )


            graph[
                "connections"
            ][
                "verified_backlinks"
            ].append(

                {

                    "source_domain":
                        source_domain,

                    "source_url":
                        source_url,

                    "source_type":
                        self.clean(
                            backlink.get(
                                "source_type"
                            )
                        ),

                    "target_url":
                        target_url,

                    "anchor_text":
                        self.clean(
                            backlink.get(
                                "anchor_text"
                            )
                        ),

                    "rel":
                        self.clean(
                            backlink.get(
                                "rel"
                            )
                        ),

                    "follow":
                        bool(
                            backlink.get(
                                "follow",
                                False
                            )
                        ),

                    "nofollow":
                        bool(
                            backlink.get(
                                "nofollow",
                                False
                            )
                        ),

                    "sponsored":
                        bool(
                            backlink.get(
                                "sponsored",
                                False
                            )
                        ),

                    "ugc":
                        bool(
                            backlink.get(
                                "ugc",
                                False
                            )
                        ),

                    "link_verified":
                        True,

                    "status":
                        "ACTIVE"

                }

            )


        graph[
            "validation"
        ][
            "verified_backlinks"
        ] = len(

            graph[
                "connections"
            ][
                "verified_backlinks"
            ]

        )


        graph[
            "validation"
        ][
            "backlink_domains"
        ] = len(
            backlink_domains
        )


        # =====================================================
        # WRITE
        # =====================================================

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


        print(
            "AUTHORITY SOURCE GRAPH CREATED V2"
        )


        for key, value in graph[
            "connections"
        ].items():

            print(
                key,
                ":",
                len(
                    value
                )
            )


        print(
            "PRODUCTS:",
            graph[
                "validation"
            ][
                "products_checked"
            ]
        )


        print(
            "SOURCES:",
            graph[
                "validation"
            ][
                "sources_found"
            ]
        )


        print(
            "BACKLINKS CHECKED:",
            graph[
                "validation"
            ][
                "backlinks_checked"
            ]
        )


        print(
            "VERIFIED BACKLINKS:",
            graph[
                "validation"
            ][
                "verified_backlinks"
            ]
        )


        print(
            "BACKLINK DOMAINS:",
            graph[
                "validation"
            ][
                "backlink_domains"
            ]
        )


        return graph


if __name__ == "__main__":

    builder = AuthoritySourceGraphBuilder()

    builder.build()
