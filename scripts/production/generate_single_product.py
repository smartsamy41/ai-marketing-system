import sys
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from engine.pipeline.content_pipeline import ContentPipeline
from engine.rendering.production_renderer import ProductionRenderer
from engine.publishing.repository_publisher import RepositoryPublisher



pipeline = ContentPipeline()

renderer = ProductionRenderer()

publisher = RepositoryPublisher()



with open(
    "data_master/catalog/product_master_44.json",
    encoding="utf-8"
) as f:

    catalog = json.load(f)



product = next(

    p for p in catalog["products"]

    if p["product_id"] == "CHK24_001"

)



result = pipeline.process(
    product
)



landing_product = result["landingpage"]


landing_html = renderer.render_landingpage(
    landing_product
)



landing_path = publisher.save_landingpage(
    "strom",
    landing_html
)



article_html = renderer.render_article(
    result["article"]
)



article_path = publisher.save_article(
    "strom-ratgeber",
    article_html
)



print("PRODUCTION CREATED")

print(landing_path)

print(article_path)
