import json

from app.geo.geo_composer import GEOComposer
from app.geo.jsonld_bridge import build_product_jsonld


composer = GEOComposer()


product = composer.build_product_entity(
    "CHK24_001"
)


if not product:

    raise Exception(
        "Produkt nicht gefunden"
    )


jsonld = build_product_jsonld(
    product
)


print(
    "GEO PIPELINE OK"
)

print(
    jsonld
)
