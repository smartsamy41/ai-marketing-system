import os


FILES = [

    "app/geo/product_entity_schema.py",

    "app/geo/entity_registry.py",

    "app/geo/fact_registry.py",

    "app/geo/geo_composer.py",

    "app/geo/jsonld_bridge.py",

    "app/geo/integration_adapter.py",

    "app/geo/geo_cache.py",

    "app/geo/geo_service.py",

    "app/geo/landingpage_hook.py"

]


print("GEO CORE AUDIT")
print("=" * 40)


ok = 0


for file in FILES:

    if os.path.exists(file):

        print(
            "OK   ",
            file
        )

        ok += 1

    else:

        print(
            "MISS ",
            file
        )


print("=" * 40)

print(
    "Files:",
    ok,
    "/",
    len(FILES)
)


if ok == len(FILES):

    print(
        "GEO CORE STATUS: READY"
    )

else:

    print(
        "GEO CORE STATUS: INCOMPLETE"
    )
