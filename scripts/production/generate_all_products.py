import sys
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from engine.pipeline.content_pipeline import ContentPipeline
from engine.rendering.production_renderer import ProductionRenderer
from engine.publishing.repository_publisher import RepositoryPublisher



def create_slug(name):

    slug = name.lower()


    replacements = {

        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss"

    }


    for old, new in replacements.items():

        slug = slug.replace(
            old,
            new
        )


    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug
    )


    slug = slug.strip("-")


    return slug




pipeline = ContentPipeline()

renderer = ProductionRenderer()

publisher = RepositoryPublisher()



with open(
    "data_master/catalog/product_master_44.json",
    encoding="utf-8"
) as f:

    catalog = json.load(f)



created = 0



for product in catalog["products"]:


    result = pipeline.process(
        product
    )



    landing_html = renderer.render_landingpage(
        result["landingpage"]
    )


    slug = create_slug(
        product["name"]
    )


    publisher.save_landingpage(
        slug,
        landing_html
    )



    article_html = renderer.render_article(
        result["article"]
    )


    publisher.save_article(
        slug + "-ratgeber",
        article_html
    )


    created += 1



print(
    "BATCH PRODUCTION FINISHED"
)

print(
    "CREATED PRODUCTS:",
    created
)
