from pathlib import Path


class RepositoryPublisher:

    def __init__(
        self,
        base_path="content_repository"
    ):

        self.base = Path(
            base_path
        )


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def slugify(value):

        return (
            str(value or "")
            .strip()
            .lower()
            .replace(" ", "-")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )


    # =========================================================
    # STANDARD LANDINGPAGE
    # =========================================================

    def save_landingpage(
        self,
        slug,
        html
    ):

        slug = self.slugify(
            slug
        )

        if not slug:
            raise ValueError(
                "Landingpage slug required"
            )

        path = (
            self.base
            / "landingpages"
            / "published"
            / f"{slug}.html"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            str(html),
            encoding="utf-8"
        )

        return str(path)


    # =========================================================
    # BLOG ARTICLE
    # =========================================================

    def save_article(
        self,
        slug,
        html
    ):

        slug = self.slugify(
            slug
        )

        if not slug:
            raise ValueError(
                "Article slug required"
            )

        path = (
            self.base
            / "articles"
            / "published"
            / f"{slug}.html"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            str(html),
            encoding="utf-8"
        )

        return str(path)


    # =========================================================
    # GEO PATH
    # =========================================================

    def get_geo_path(
        self,
        silo,
        category,
        location_slug
    ):

        silo = self.slugify(
            silo
        )

        category = self.slugify(
            category
        )

        location_slug = self.slugify(
            location_slug
        )

        if not all([
            silo,
            category,
            location_slug
        ]):

            raise ValueError(
                "silo, category and location_slug required"
            )

        return (
            self.base
            / "geo"
            / "published"
            / silo
            / category
            / location_slug
            / "index.html"
        )


    # =========================================================
    # SAVE GEO PAGE
    # =========================================================

    def save_geo_page(
        self,
        silo,
        category,
        location_slug,
        html
    ):

        path = self.get_geo_path(
            silo,
            category,
            location_slug
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            str(html),
            encoding="utf-8"
        )

        return str(path)


    # =========================================================
    # GEO EXISTS
    # =========================================================

    def geo_page_exists(
        self,
        silo,
        category,
        location_slug
    ):

        return self.get_geo_path(
            silo,
            category,
            location_slug
        ).exists()


    # =========================================================
    # LIST GEO PAGES
    # =========================================================

    def list_geo_pages(self):

        root = (
            self.base
            / "geo"
            / "published"
        )

        if not root.exists():
            return []

        return [
            str(path)
            for path in sorted(
                root.glob(
                    "**/index.html"
                )
            )
        ]


    # =========================================================
    # DELETE GEO PAGE
    # =========================================================

    def delete_geo_page(
        self,
        silo,
        category,
        location_slug
    ):

        path = self.get_geo_path(
            silo,
            category,
            location_slug
        )

        if not path.exists():

            return {
                "status": "NOT_FOUND",
                "path": str(path)
            }

        path.unlink()

        current = path.parent

        geo_root = (
            self.base
            / "geo"
            / "published"
        )

        while (
            current != geo_root
            and current.exists()
        ):

            try:
                current.rmdir()

            except OSError:
                break

            current = current.parent

        return {
            "status": "DELETED",
            "path": str(path)
        }


    # =========================================================
    # VALIDATED GEO PUBLISH
    # =========================================================

    def publish_geo_node(
        self,
        node,
        html
    ):

        validation = (
            node.get(
                "validation",
                {}
            )
            or {}
        )

        required = [
            "real_location",
            "source_verified",
            "wikidata_verified",
            "product_match",
            "category_match",
            "search_intent_match",
            "partner_compliant",
            "local_data_available",
            "unique_content"
        ]

        failed = [
            field
            for field in required
            if validation.get(field) is not True
        ]

        if failed:

            return {
                "status":
                    "BLOCKED",

                "reason":
                    "GEO_QUALITY_SHIELD_FAILED",

                "failed":
                    failed
            }


        silo = self.slugify(
            node.get("silo")
        )

        category = self.slugify(
            node.get("category")
        )

        location_slug = self.slugify(
            node.get("location_name")
        )

        if not all([
            silo,
            category,
            location_slug
        ]):

            return {
                "status":
                    "BLOCKED",

                "reason":
                    "MISSING_GEO_ROUTING_DATA"
            }


        path = self.save_geo_page(
            silo,
            category,
            location_slug,
            html
        )


        url = (
            "https://freebasics.online/"
            f"{silo}/"
            f"{category}/"
            f"{location_slug}/"
        )


        return {
            "status":
                "PUBLISHED",

            "path":
                path,

            "url":
                url
        }


if __name__ == "__main__":

    publisher = RepositoryPublisher()

    print(
        "RepositoryPublisher READY"
    )

    print(
        "GEO PAGES:",
        len(
            publisher.list_geo_pages()
        )
    )
