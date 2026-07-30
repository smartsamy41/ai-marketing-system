from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from engine.pipeline.content_pipeline import ContentPipeline
from engine.content_repository_writer import ContentRepositoryWriter
from engine.content_generation.landingpage_builder import LandingPageBuilder


pipeline = ContentPipeline()

writer = ContentRepositoryWriter()


product = {
    "product_id": "CHK24_001",
    "name": "Strom",
    "category": "Energie",
    "partner": "check24"
}


result = pipeline.process(
    product
)


if result.get("status") != "READY":
    raise Exception(result)


landingpage = result.get(
    "landingpage"
)

article = result.get(
    "article"
)


print(
    "Landingpage:",
    landingpage.get("status")
)


print(
    "Article:",
    article.get("status")
)


landing_html = result.get(
    "landingpage_html"
)


article_html = result.get(
    "article_html"
)


landing_file = writer.save_landingpage(
    "CHK24_001",
    landing_html
)


article_file = writer.save_article(
    "CHK24_001",
    article_html
)


print()
print("CREATED:")
print(landing_file)
print(article_file)
