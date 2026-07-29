from engine.content_pipeline_adapter import ContentPipelineAdapter
import json


adapter = ContentPipelineAdapter()


product = {
    "product_id": "CHK24_001",
    "name": "Strom",
    "partner": "check24",
    "category": "Energie"
}


result = adapter.generate(
    product
)


print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)
