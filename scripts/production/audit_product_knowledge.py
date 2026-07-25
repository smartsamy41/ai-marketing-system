import json


files = [
    "data_master/catalog/product_master_44.json",
    "data_master/geo_and_entities/primary_sources_index.json",
    "data_master/geo_and_entities/llm_knowledge_chunks.json"
]


for file in files:
    print("\n==========")
    print(file)

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    if "products" in data:
        print("Products:", len(data["products"]))

    if "chunks" in data:
        print("Chunks:", len(data["chunks"]))

    if "sources" in data:
        print("Sources:", len(data["sources"]))

    print("Status:", data.get("status"))
