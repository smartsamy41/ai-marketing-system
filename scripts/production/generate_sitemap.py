from pathlib import Path
from datetime import datetime, timezone


DOMAIN = "https://freebasics.online"


OUTPUT = Path(
    "public_web_assets/sitemap.xml"
)


URLS = []


def add_url(url):
    URLS.append(url)



# Homepage
add_url(f"{DOMAIN}/")



# Landingpages
landingpages = Path(
    "content_repository/landingpages/published"
)

for file in sorted(landingpages.glob("*.html")):
    slug = file.stem
    add_url(
        f"{DOMAIN}/angebote/{slug}"
    )



# Blogartikel
articles = Path(
    "content_repository/articles/published"
)

for file in sorted(articles.glob("*.html")):
    slug = file.stem
    add_url(
        f"{DOMAIN}/blog/{slug}"
    )



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



OUTPUT.write_text(
    "\n".join(xml),
    encoding="utf-8"
)



print("SITEMAP CREATED")
print("URLS:", len(URLS))
print("FILE:", OUTPUT)

