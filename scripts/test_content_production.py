from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from engine.content_generation.landingpage_builder import LandingpageBuilder
from engine.content_generation.blog_article_builder import BlogArticleBuilder
from engine.content_repository_writer import ContentRepositoryWriter


product = {
    "product_id": "CHK24_001",
    "name": "Strom",
    "category": "Energie",
    "partner": "check24",
    "description": "Informationen zu Stromtarifen",
    "tracking_url": "#",
    "content": "Informationen und Wissensinhalte zum Thema Strom."
}


writer = ContentRepositoryWriter()


# Landingpage Produktion

landing_builder = LandingpageBuilder()

landingpage = landing_builder.build(product)

print(
    "Landingpage Validation:",
    landing_builder.validate(landingpage)
)

landing_html = landing_builder.render(
    landingpage
)

landing_file = writer.save_landingpage(
    "CHK24_001",
    landing_html
)


# Blogartikel Produktion

article_builder = BlogArticleBuilder()

article = article_builder.build(product)

print(
    "Article Validation:",
    article_builder.validate(article)
)

article_html = article_builder.render(
    article
)

article_file = writer.save_article(
    "CHK24_001",
    article_html
)


print()
print("CREATED:")
print(landing_file)
print(article_file)
