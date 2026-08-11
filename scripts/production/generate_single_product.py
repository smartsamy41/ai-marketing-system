import sys
import json
import re
import unicodedata
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from engine.pipeline.content_pipeline import ContentPipeline
from engine.rendering.production_renderer import ProductionRenderer
from engine.publishing.repository_publisher import RepositoryPublisher



def normalize_slug(text):

    text = str(text).lower()


    replacements = {

        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss"

    }


    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )


    text = unicodedata.normalize(
        "NFKD",
        text
    )


    text = text.encode(
        "ascii",
        "ignore"
    ).decode(
        "ascii"
    )


    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )


    text = re.sub(
        r"-+",
        "-",
        text
    )


    return text.strip("-")



PRODUCT_ID = (

    sys.argv[1]

    if len(sys.argv) > 1

    else

    "CHK24_001"

)



pipeline = ContentPipeline()

renderer = ProductionRenderer()

publisher = RepositoryPublisher()



with open(
    "data_master/catalog/product_master_44.json",
    encoding="utf-8"
) as f:

    catalog = json.load(f)



product = next(

    p

    for p in catalog["products"]

    if p["product_id"] == PRODUCT_ID

)



print("PRODUCT:")
print(product["product_id"])
print(product["name"])



result = pipeline.process(
    product
)



if result.get("status") != "READY":

    print(
        "ERROR:"
    )

    print(
        result
    )

    sys.exit(1)



landing_product = result["landingpage"]



landing_html = renderer.render_landingpage(
    landing_product
)



slug = normalize_slug(
    product["name"]
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

print(
    "PRODUCTION CREATED"
)

print(
    landing_path
)

print(
    article_path
)
