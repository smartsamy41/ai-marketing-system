import json
import re
import unicodedata
from pathlib import Path
import sys


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



pipeline = ContentPipeline()

renderer = ProductionRenderer()

publisher = RepositoryPublisher()



with open(
    "data_master/catalog/product_master_44.json",
    encoding="utf-8"
) as f:

    catalog = json.load(f)



products = catalog["products"]



success = 0

failed = 0



print()

print("=" * 60)

print("PRODUCTION TEST ALL PRODUCTS")

print("=" * 60)



for product in products:


    print()

    print("=" * 60)

    print(
        "TEST:",
        product["product_id"],
        product["name"]
    )

    print("=" * 60)



    try:


        result = pipeline.process(
            product.copy()
        )



        if result.get("status") != "READY":

            print(
                "FAILED PIPELINE"
            )

            failed += 1

            continue



        slug = normalize_slug(
            product["name"]
        )



        landing_html = renderer.render_landingpage(
            result["landingpage"]
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



        if (
            Path(landing_path).exists()
            and
            Path(article_path).exists()
        ):

            print(
                "OK"
            )

            success += 1


        else:

            print(
                "FAILED FILE CHECK"
            )

            failed += 1



    except Exception as e:


        print(
            "ERROR:",
            e
        )

        failed += 1





print()

print("=" * 60)

print("FINAL REPORT")

print("=" * 60)

print(
    "SUCCESS:",
    success
)

print(
    "FAILED:",
    failed
)
