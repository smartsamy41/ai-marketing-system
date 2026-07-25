import urllib.request

from app.geo.schema_guard import schema_status


URL = "https://freebasics.online/lp/CHK24_001"


html = urllib.request.urlopen(
    URL
).read().decode(
    "utf-8"
)


result = schema_status(
    html
)


print(
    "LIVE SCHEMA AUDIT"
)

print(
    "URL:",
    URL
)

print(
    "RESULT:"
)

print(
    result
)


if result["product_schema_count"] > 1:

    print(
        "WARNING: Multiple Product schemas detected"
    )

else:

    print(
        "SCHEMA STATUS: CLEAN"
    )
