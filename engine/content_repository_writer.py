from pathlib import Path


class ContentRepositoryWriter:

    def __init__(
        self,
        base_path="content_repository"
    ):
        self.base_path = Path(base_path)


    def save_landingpage(
        self,
        product_id,
        html
    ):

        folder = (
            self.base_path
            / "landingpages"
            / "published"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file = folder / f"{product_id}.html"

        file.write_text(
            html,
            encoding="utf-8"
        )

        return str(file)


    def save_article(
        self,
        product_id,
        html
    ):

        folder = (
            self.base_path
            / "articles"
            / "approved"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file = folder / f"{product_id}.html"

        file.write_text(
            html,
            encoding="utf-8"
        )

        return str(file)


if __name__ == "__main__":

    writer = ContentRepositoryWriter()

    print(
        writer.save_landingpage(
            "TEST_001",
            "<html>Landingpage Test</html>"
        )
    )

    print(
        writer.save_article(
            "TEST_001",
            "<html>Article Test</html>"
        )
    )
