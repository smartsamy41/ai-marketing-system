from pathlib import Path


DOMAIN = "https://freebasics.online"

OUTPUT = Path(
    "public_web_assets/sitemap.xml"
)

URLS = []


def add_url(url):

    if not url:
        return

    if url not in URLS:
        URLS.append(url)


# =========================================================
# HOMEPAGE
# =========================================================

add_url(
    f"{DOMAIN}/"
)


# =========================================================
# STANDARD LANDINGPAGES
# =========================================================

landingpages = Path(
    "content_repository/landingpages/published"
)

for file in sorted(
    landingpages.glob("*.html")
):

    slug = file.stem

    add_url(
        f"{DOMAIN}/angebote/{slug}"
    )


# =========================================================
# BLOG ARTICLES
# =========================================================

articles = Path(
    "content_repository/articles/published"
)

for file in sorted(
    articles.glob("*.html")
):

    slug = file.stem

    add_url(
        f"{DOMAIN}/blog/{slug}"
    )


# =========================================================
# VALIDATED GEO PAGES
# =========================================================

geo_root = Path(
    "content_repository/geo/published"
)

if geo_root.exists():

    for file in sorted(
        geo_root.glob(
            "**/index.html"
        )
    ):

        relative = file.relative_to(
            geo_root
        )

        parts = relative.parts

        # erwartet:
        # silo/category/location/index.html

        if len(parts) != 4:
            continue

        silo = parts[0]
        category = parts[1]
        location = parts[2]

        add_url(
            f"{DOMAIN}/"
            f"{silo}/"
            f"{category}/"
            f"{location}/"
        )


# =========================================================
# XML
# =========================================================

xml = []

xml.append(
    '<?xml version="1.0" encoding="UTF-8"?>'
)

xml.append(
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
)

for url in URLS:

    xml.append(
        "<url>"
    )

    xml.append(
        f"<loc>{url}</loc>"
    )

    xml.append(
        "</url>"
    )

xml.append(
    "</urlset>"
)


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT.write_text(
    "\n".join(xml),
    encoding="utf-8"
)


print(
    "SITEMAP CREATED"
)

print(
    "URLS:",
    len(URLS)
)

print(
    "FILE:",
    OUTPUT
)

print(
    "GEO URL PRESENT:",
    (
        "https://freebasics.online/"
        "energie/strom/luebeck/"
    )
    in URLS
)
