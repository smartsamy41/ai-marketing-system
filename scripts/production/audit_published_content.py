from pathlib import Path


landingpages = Path(
    "content_repository/landingpages/published"
)

articles = Path(
    "content_repository/articles/published"
)


def check_file(path):

    content = path.read_text(
        encoding="utf-8"
    )

    checks = {

        "canonical":
            "rel=\"canonical\"" in content,

        "schema":
            "application/ld+json" in content,

        "advertisement":
            "Werbung / Anzeige" in content,

        "product_id":
            "productID" in content,

    }

    return checks



print("=== LANDINGPAGES ===")

landing_ok = 0

for file in sorted(
    landingpages.glob("*.html")
):

    result = check_file(file)

    if all(result.values()):
        landing_ok += 1


print(
    "PASS:",
    landing_ok,
    "/",
    len(list(landingpages.glob("*.html")))
)



print()
print("=== ARTICLES ===")


article_ok = 0

for file in sorted(
    articles.glob("*.html")
):

    result = {

        "canonical":
            "rel=\"canonical\"" in file.read_text(encoding="utf-8"),

        "schema":
            "application/ld+json" in file.read_text(encoding="utf-8"),

        "author":
            "Autor:" in file.read_text(encoding="utf-8"),

        "reviewer":
            "Geprüft von:" in file.read_text(encoding="utf-8"),

    }


    if all(result.values()):
        article_ok += 1



print(
    "PASS:",
    article_ok,
    "/",
    len(list(articles.glob("*.html")))
)
