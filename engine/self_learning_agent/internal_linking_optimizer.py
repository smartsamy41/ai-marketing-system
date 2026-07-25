class InternalLinkingOptimizer:

    def __init__(
        self,
        source="knowledge_graph"
    ):

        self.source = source


    def suggest_links(
        self,
        article,
        products
    ):

        links = []

        for product in products:

            links.append(
                {
                    "from": article.get("slug"),
                    "to": product.get("product_id"),
                    "reason": "topic_relation",
                    "status": "suggested"
                }
            )

        return {
            "source": self.source,
            "links": links,
            "count": len(links)
        }


    def validate_link(
        self,
        link
    ):

        return {
            "link": link,
            "valid": True
        }


if __name__ == "__main__":

    optimizer = InternalLinkingOptimizer()

    print(
        optimizer.suggest_links(
            {
                "slug": "dsl-ratgeber"
            },
            [
                {
                    "product_id": "CHK24_004"
                }
            ]
        )
    )
