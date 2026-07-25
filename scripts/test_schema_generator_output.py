from app.schema_generator import generate_product_schema

schema = generate_product_schema(
    name="Strom",
    description="Strom vergleichen und passende Angebote prüfen.",
    url="https://freebasics.online/lp/CHK24_001"
)

print(schema)
print()
print("COUNT:", schema.count('"@type": "Product"'))

