import json
from pathlib import Path


OUTPUT_FILE = "knowledge/entities/products.json"


def build_registry():

    registry = {
        "version": "1.0",
        "system": "FREE BASICS AI MARKETING SYSTEM",
        "description": "Product Entity Registry for GEO and Knowledge Graph",
        "generated_by": "AI Entity Builder",
        "status": "READY_FOR_IMPORT",
        "products": []
    }


    output = Path(OUTPUT_FILE)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    output.write_text(
        json.dumps(
            registry,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print("ENTITY REGISTRY READY")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    build_registry()
