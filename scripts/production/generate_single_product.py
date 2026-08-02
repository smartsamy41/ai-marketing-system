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



# HIER DAS PRODUKT ÄNDERN
PRODUCT_ID = "CHK24_004"



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

    if p["product_id"] == PRODUCT_ID

)



print("PRODUCT:")
print(product["product_id"])
print(product["name"])



result = pipeline.process(
    product
)



landing_product = result["landingpage"]


landing_html = renderer.render_landingpage(
    landing_product
)



slug = (
    product["name"]
    .lower()
    .replace("ä","ae")
    .replace("ö","oe")
    .replace("ü","ue")
    .replace(" ","-")
)



landing_path = publisher.save_landingpage(
    slug,
    landing_html
)



article_html = renderer.render_article(
    result["article"]
)



article_path = publisher.save_article(
    slug + "-ratgeber",
    article_html
)



print()
print("PRODUCTION CREATED")
print(landing_path)
print(article_path)
