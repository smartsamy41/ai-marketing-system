from pathlib import Path


class RepositoryPublisher:


    def __init__(self):

        self.base = Path(
            "content_repository"
        )



    def save_landingpage(
        self,
        slug,
        html
    ):

        path = (
            self.base
            /
            "landingpages"
            /
            "published"
            /
            f"{slug}.html"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            html,
            encoding="utf-8"
        )

        return str(path)



    def save_article(
        self,
        slug,
        html
    ):

        path = (
            self.base
            /
            "articles"
            /
            "published"
            /
            f"{slug}.html"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            html,
            encoding="utf-8"
        )

        return str(path)



if __name__ == "__main__":


    publisher = RepositoryPublisher()


    print(
        publisher.save_landingpage(
            "strom",
            "<html>Strom Test</html>"
        )
    )


    print(
        publisher.save_article(
            "strom-ratgeber",
            "<html>Artikel Test</html>"
        )
    )
