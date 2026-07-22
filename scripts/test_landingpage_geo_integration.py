from app.geo.landingpage_hook import GEOLandingpageHook


hook = GEOLandingpageHook()


product_id = "CHK24_001"


schema = hook.schema_for_product(
    product_id
)


print(
    "LANDINGPAGE GEO INTEGRATION TEST"
)

print(
    "PRODUCT:",
    product_id
)


if schema:

    print(
        "STATUS: READY"
    )

    print(
        schema
    )

else:

    print(
        "STATUS: NO SCHEMA"
    )
